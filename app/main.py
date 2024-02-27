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

from shared.services.db_service import Service_bdd
from shared.models.user import User
from shared.models.group import Group
from shared.models.message import Message
from shared.models.media import Media

# FastAPI instance
app = FastAPI()

load_dotenv()

# Configurer le système de journalisation
logging.basicConfig(filename=os.getenv('LOG_FILE'), level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

bdd_service = Service_bdd()

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


@app.post("/message/socket/init")
def init_message_socket():
    logging.info("Initialisation du socket de message.")
    return bdd_service.init_message_socket()


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

@app.post("/group/new")
def create_group(name):
    logging.info("Création d'un groupe.")
    group = Group(name)
    group_id = bdd_service.create_group(group)
    return {"id": group_id, "group": vars(group)}


@app.post("/group/rename/{group_id}")
def rename_group(group_id: int, new_name: str):
    logging.info(f"Renommage du groupe ID: {group_id} en {new_name}.")
    bdd_service.rename_group(group_id, new_name)
    return {"new_name": new_name}


@app.delete("/group/remove_user/{group_id}/{user_id}")
def remove_group(group_id: int, user_id: int):
    logging.info(f"Suppression de l'utilisateur ID: {user_id} du groupe ID: {group_id}.")
    bdd_service.remove_user_from_group(group_id, user_id)
    return {"user_removed": user_id, "group": group_id}


@app.post("/group/add_user/{group_id}/{user_id}")
def add_user_to_group(group_id: int, user_id: int):
    logging.info(f"Ajout de l'utilisateur ID: {user_id} au groupe ID: {group_id}.")
    bdd_service.add_user_to_group(user_id, group_id)
    return {"user_added": user_id, "group": group_id}


@app.get("/group/{group_id}")
def get_group(group_id: int):
    logging.info(f"Récupération du groupe ID: {group_id}.")
    return {"group": vars(bdd_service.get_group(group_id))}


@app.get("/group/get_by_user/{user_id}")
def get_groups_by_user(user_id: int):
    logging.info(f"Récupération des groupes de l'utilisateur ID: {user_id}.")
    return {
            "user": user_id,
            "groups": [vars(element) for element in bdd_service.get_groups_user(user_id)]
            }


@app.get("/group/get_users/{group_id}")
def get_users_in_group(group_id: int):
    logging.info(f"Récupération des utilisateurs dans le groupe ID: {group_id}.")
    return {
            "group": group_id,
            "users": [vars(element) for element in bdd_service.get_users_in_group(group_id)]
            }


# User Routes
@app.get("/user/get/{user_id}")
async def get_user(user_id: int):
    return {"user": vars(bdd_service.get_user(user_id))}


@app.get("/user/auth/{user_id}")
async def get_user_auth(auth_id: int):
    return {
            "auth": auth_id,
            "user": vars(bdd_service.get_user_auth(auth_id))
            }


@app.post("/user/new")
def create_user(name: str,
                first_name: str,
                email: str,
                join_date: int,
                auth_id: str,
                ):
    user = User(
            name,
            first_name,
            email,
            join_date,
            auth_id
            )
    user_id = bdd_service.create_user()
    return {"id": user_id, "user": vars(user)}



@app.put("/user/modify/{user_id}")
def modify_user(
        user_id: int,
        new_name: str,
        new_first_name: str,
        new_email: str
        ):
    bdd_service.set_user(
            user_id,
            User(new_name, new_first_name, new_email, 0, '')
            )
    return {
            "new_name": new_name,
            "new_first_name": new_first_name,
            "new_email": new_email,
            }

@app.delete("/user/delete/{user_id}")
def delete_user(user_id: int):
    bdd_service.delete_user(user_id)
    return {"user_deleted": user_id}


@app.get("/user/get_by_email/{email}")
def get_by_email(email: str):
    return {"user": vars(bdd_service.get_user_email(email))}


@app.get("/user/get_all")
def get_all_users():
    return {"users": [vars(element) for element in bdd_service.get_all_users()]}

# Message Routes

@app.delete("/message/delete/{message_id}")
def delete_message(message_id: int):
    logging.info(f"Suppression du message ID: {message_id}.")
    bdd_service.delete_message(message_id)
    return {"message_deleted": message_id}


@app.get("/message/get/{message_id}")
def get_message(message_id: int):
    logging.info(f"Récupération du message ID: {message_id}.")
    return {"message": vars(bdd_service.get_message(message_id))}


@app.post("/message/create")
def create_message(
        content: str,
        sender_id: str,
        receiver_group_id: str,
        date: int
        ):
    logging.info("Création d'un nouveau message.")
    message = Message(
            content,
            sender_id,
            receiver_group_id,
            date
            )
    message_id = bdd_service.create_message()
    return {"message_id": message_id, "message": vars(message)}

@app.get("/media/get/{media_id}")
def get_media(media_id: int):
    logging.info(f"Récupération du média ID: {media_id}.")
    return {"media": vars(bdd_service.get_media(media_id))}


@app.get("/media/get_by_message/{message_id}")
def get_media_by_message(message_id: int):
    logging.info(f"Récupération du média pour le message ID: {message_id}.")
    return {
            "message_id": message_id,
            "medias": [vars(element) for element in bdd_service.get_medias_message(message_id)]
            }
