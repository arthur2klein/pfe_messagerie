# main.py
import logging
import os
from datetime import datetime, timedelta
from typing import List

from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from services.service_bdd import Service_bdd

# FastAPI instance
app = FastAPI()

load_dotenv()

# Configurer le système de journalisation
logging.basicConfig(filename=os.getenv('LOG_FILE'), level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Database

DATABASE_URL = "postgresql://" + os.getenv('PG_USER') + ":" + os.getenv('PG_PASSWORD') + "@" + os.getenv(
    'PG_HOST') + "/" + os.getenv('PG_DATABASE')

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base(metadata=MetaData())

# Call services' module
bdd_service = Service_bdd()
# Initialisation des tables en BD
bdd_service.DB_initialize()


# Models
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    name = Column(String)
    email = Column(String)
    auth_id = Column(Integer)
    hashed_password = Column(String)
    join_date = Column(DateTime, default=datetime.utcnow)


class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    # Relationship with users
    users = relationship("User", back_populates="Group")


class UserInGroup(Base):
    __tablename__ = "users_in_group"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    group_id = Column(Integer, ForeignKey("groups.id"))


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    sender_id = Column(Integer, ForeignKey("users.id"))
    receiver_group_id = Column(Integer, ForeignKey("groups.id"))
    date = Column(DateTime, default=datetime.utcnow)


class Media(Base):
    __tablename__ = "medias"
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)
    link = Column(String)
    message_id = Column(Integer, ForeignKey("messages.id"))


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# JWT Token Settings
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')

users = {}
groups = {}
messages = []
media_items = []

# WebSocket connections (replace with your actual storage)
websocket_connections = {}


# Function to create JWT tokens
def create_access_token(data: dict):
    to_encode = data.copy()
    expires = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expires})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# OAuth2PasswordBearer for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# API Route for login
@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordBearer = Depends()):
    # Validate user credentials (this is a simplified example)
    # In a real-world scenario, you would verify the credentials against a database
    # and check the hashed password, etc.
    user = {"sub": form_data.username}
    access_token = create_access_token(data=user)
    return {"access_token": access_token, "token_type": "bearer"}


# Function to get the current user from the token
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return username


# API Route for protected data
@app.get("/protected-data")
async def get_protected_data(current_user: str = Depends(get_current_user)):
    return {"message": f"Hello, {current_user}, here is your protected data."}


# WebSocket path operation for user iteration
@app.websocket("/ws/user_iterator/{user_id}")
async def user_iterator_ws(websocket: WebSocket, user_id: int):
    await websocket.accept()

    try:
        while True:
            # Get the next user data (replace with your actual logic)
            user = get_next_user(user_id)

            # Send user data to the client
            await websocket.send_json(user.dict())

    except WebSocketDisconnect:
        # Handle disconnect
        pass


# WebSocket path operation for message handling
@app.websocket("/ws/message/{user_id}")
async def message_ws(websocket: WebSocket, user_id: int):
    await websocket.accept()

    # Store the WebSocket connection for later use
    websocket_connections[user_id] = websocket

    try:
        while True:
            # Receive and handle messages from the client
            data = await websocket.receive_json()
            bdd_service.handle_message(data, user_id)

    except WebSocketDisconnect:
        # Handle disconnect
        del websocket_connections[user_id]


# RESTful API routes

# Group Routes

@app.get("/group/{group_id}")
async def get_group(group_id: int):
    return bdd_service.get_group(group_id)


# Group Routes

@app.post("/group/new")
def create_group():
    logging.info("Création d'un groupe.")
    return bdd_service.create_group()


@app.post("/group/rename/{group_id}")
def rename_group(group_id: int, new_name: str):
    logging.info(f"Renommage du groupe ID: {group_id} en {new_name}.")
    return bdd_service.rename_group(group_id, new_name)


@app.delete("/group/remove_user/{group_id}/{user_id}")
def remove_group(group_id: int, user_id: int):
    logging.info(f"Suppression de l'utilisateur ID: {user_id} du groupe ID: {group_id}.")
    return bdd_service.remove_user_from_group(group_id, user_id)


@app.post("/group/add_user/{group_id}/{user_id}")
def add_user_to_group(group_id: int, user_id: int):
    logging.info(f"Ajout de l'utilisateur ID: {user_id} au groupe ID: {group_id}.")
    return bdd_service.add_user_to_group(user_id, group_id)


@app.get("/group/get/{group_id}")
def get_group(group_id: int):
    logging.info(f"Récupération du groupe ID: {group_id}.")
    return bdd_service.get_group(group_id)


@app.get("/group/get_by_user/{user_id}", response_model=List[Group])
def get_groups_by_user(user_id: int):
    logging.info(f"Récupération des groupes de l'utilisateur ID: {user_id}.")
    return bdd_service.get_groups_user(user_id)


@app.get("/group/get_users/{group_id}", response_model=List[User])
def get_users_in_group(group_id: int):
    logging.info(f"Récupération des utilisateurs dans le groupe ID: {group_id}.")
    return bdd_service.get_users_in_group(group_id)


# User Routes
@app.get("/user/get/{user_id}")
async def get_user(user_id: int):
    return bdd_service.get_user(user_id)


@app.get("/user/auth/{user_id}")
async def get_user_auth(auth_id: int):
    return bdd_service.get_user_auth(auth_id)


@app.post("/user/new")
def create_user(user: User):
    return bdd_service.create_user(user)


@app.put("/user/modify/{user_id}")
def modify_user(user_id: int, new_data: User):
    return bdd_service.set_user(user_id, new_data)


@app.delete("/user/delete/{user_id}")
def modify_user(user_id: int):
    return bdd_service.delete_user(user_id)


@app.get("/user/get_by_email/{email}")
def modify_user(email: str):
    return bdd_service.get_user_email(email)


@app.get("/user/get_all", response_model=List[User])
def get_all_users():
    return bdd_service.get_all_users()


# ... Implement other user routes similarly

# Message Routes

@app.delete("/message/delete/{message_id}")
def delete_message(message_id: int):
    logging.info(f"Suppression du message ID: {message_id}.")
    return bdd_service.delete_message(message_id)


@app.get("/message/get/{message_id}")
def get_message(message_id: int):
    logging.info(f"Récupération du message ID: {message_id}.")
    return bdd_service.get_message(message_id)


@app.post("/message/create")
def create_message():
    logging.info("Création d'un nouveau message.")
    return bdd_service.create_message()


@app.post("/message/user_iterator/init")
def init_user_iterator():
    logging.info("Initialisation de l'itérateur d'utilisateur.")
    return bdd_service.init_user_iterator()


@app.get("/message/user_iterator/next")
def get_next_user():
    logging.info("Récupération de l'utilisateur suivant.")
    return bdd_service.get_next_user()


@app.post("/message/socket/init")
def init_message_socket():
    logging.info("Initialisation du socket de message.")
    return bdd_service.init_message_socket()


@app.get("/media/get/{media_id}")
def get_media(media_id: int):
    logging.info(f"Récupération du média ID: {media_id}.")
    return bdd_service.get_media(media_id)


@app.get("/media/get_by_message/{message_id}")
def get_media_by_message(message_id: int):
    logging.info(f"Récupération du média pour le message ID: {message_id}.")
    return bdd_service.get_media_by_message(message_id)


# Media Routes

@app.get("/media/get/{media_id}")
def get_media(media_id: int):
    # Implement logic to retrieve media by ID
    return {"media": "Media retrieved successfully"}


# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
