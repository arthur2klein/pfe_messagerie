import logging
import os
from datetime import datetime, timedelta
from typing import List, Annotated, Union

from dotenv import load_dotenv
from fastapi import Request, FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect, Body
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from jose import JWTError, jwt
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from shared.services.db_service import Service_bdd
from shared.models.user import User
from shared.models.group import Group
from shared.models.message import Message
from shared.models.media import Media
from shared.exceptions.database_exception import DatabaseException
from shared.services.authen import AuthService

# FastAPI instance
app = FastAPI()

app.add_middleware(
        CORSMiddleware,
        allow_origins = ["*"],
        allow_credentials = True,
        allow_methods = ["*"],
        allow_headers = ["*"],
        )

load_dotenv()

# Configurer le système de journalisation
logging.basicConfig(filename=os.getenv('LOG_FILE'), level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

bdd_service = Service_bdd()
auth_service = AuthService()

# JWT Token Settings
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')

active_connections: set = set()

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
    try:
        # Validate user credentials (this is a simplified example)
        # In a real-world scenario, you would verify the credentials against a database
        # and check the hashed password, etc.
        user = {"sub": form_data.username}
        access_token = create_access_token(data=user)
        res = {"access_token": access_token, "token_type": "bearer"}
    except DatabaseException as e:
        res = {"error": str(e)}
    return res

@app.post("/test")
async def test_query(query: Annotated[str, Body()]):
    try:
        statusOrId = bdd_service.fetch_query(query)
        res = {"response": statusOrId}
    except DatabaseException as e:
        res = {"error": str(e)}
    return res

@app.get("/tables")
async def test_tables():
    try:
        statusOrId = bdd_service.verify_tables()
        res = {"tables": statusOrId}
    except DatabaseException as e:
        res = {"error": str(e)}
    return res

@app.post("/auth/login")
async def auth_account(
        email: Annotated[str, Body()],
        password: Annotated[str, Body()]
        ):
    try:
        successful, statusOrId = auth_service.login(email, password)
        if not(successful):
            res = {"error": statusOrId}
        else:
            res = {"auth_id": statusOrId}
    except DatabaseException as e:
        res = {"error": str(e)}
    return res

@app.post("/auth/delete")
async def delete_account(email: Annotated[str, Body()]):
    try:
        successful, statusOrId = auth_service.delete_account(email)
        if not(successful):
            res = {"error": statusOrId}
        else:
            res = {"email": email}
    except DatabaseException as e:
        res = {"error": str(e)}
    return res

@app.post("/auth/create")
async def create_account(
        email: Annotated[str, Body()],
        password: Annotated[str, Body()]
        ):
    try:
        successful, statusOrId = auth_service.create_account(email, password)
        if not(successful):
            res = {"error": statusOrId}
        else:
            res = {"auth_id": statusOrId}
    except DatabaseException as e:
        res = {"error": str(e)}
    return res

@app.post("/auth/change")
async def change_account(
        old_email: Annotated[str, Body()],
        email: Annotated[str, Body()],
        password: Annotated[str, Body()]
        ):
    try:
        successful, statusOrId = auth_service.change_account(old_email, email, password)
        if not(successful):
            res = {"error": statusOrId}
        else:
            res = {"email": email}
    except DatabaseException as e:
        res = {"error": str(e)}
    return res

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
    try:
        res = {"message": f"Hello, {current_user}, here is your protected data."}
    except DatabaseException as e:
        res = {"error": str(e)}
    return res


@app.post("/message/socket/init")
def init_message_socket():
    try:
        logging.info("Initialisation du socket de message.")
        res = bdd_service.init_message_socket()
    except DatabaseException as e:
        res = {"error": str(e)}
    return res



@app.websocket("/ws/message/{group_id}")
async def message_ws(websocket: WebSocket, group_id: str):
    print("Accepting socket")
    await websocket.accept()
    print("Socket accepted")
    active_connections.add((websocket, group_id))
    try:
        while True:
            print('WS: waiting for data')
            data = await websocket.receive_text()
            print(f'WS: Received data {data}')
            for connection, connection_group_id in active_connections.copy():
                if connection_group_id == group_id:
                    print(f'WS: Send data {data} once.')
                    await connection.send_text(data)
    except WebSocketDisconnect:
        active_connections.remove((websocket, group_id))
        await websocket.close()


# RESTful API routes


# Group Routes

@app.post("/group/new")
def create_group(name: Annotated[str, Body()]):
    try:
        logging.info("Création d'un groupe.")
        group = Group(name)
        group_id = bdd_service.create_group(group)
        res = {"id": group_id, "group": vars(group)}
    except DatabaseException as e:
        res = {"error": str(e)}
    return res


@app.post("/group/rename/{group_id}")
def rename_group(group_id: str, new_name: Annotated[str, Body()]):
    try:
        logging.info(f"Renommage du groupe ID: {group_id} en {new_name}.")
        bdd_service.rename_group(group_id, new_name)
        res = {"new_name": new_name}
    except DatabaseException as e:
        res = {"error": str(e)}
    return res


@app.delete("/group/remove_user/{group_id}/{user_id}")
def remove_group(group_id: str, user_id: str):
    try:
        logging.info(
                f"Suppression de l'utilisateur ID: "
                f"{user_id} du groupe ID: {group_id}."
                )
        bdd_service.remove_user_from_group(group_id, user_id)
        res = {"user_removed": user_id, "group": group_id}
    except DatabaseException as e:
        res = {"error": str(e)}
    return res

@app.post("/group/add_user/{group_id}/{user_id}")
def add_user_to_group(group_id: str, user_id: str):
    try:
        logging.info(
                f"Ajout de l'utilisateur ID: "
                f"{user_id} au groupe ID: {group_id}."
                )
        bdd_service.add_user_to_group(user_id, group_id)
        res = {"user_added": user_id, "group": group_id}
    except DatabaseException as e:
        res = {"error": str(e)}
    return res


@app.get("/group/{group_id}")
def get_group(group_id: str):
    try:
        logging.info(f"Récupération du groupe ID: {group_id}.")
        group_or_none = bdd_service.get_group(group_id)
        if (group_or_none == None):
            return {}
        res = {"group": vars(group_or_none)}
    except DatabaseException as e:
        res = {"error": str(e)}
    return res


@app.get("/group/get_by_user/{user_id}")
def get_groups_by_user(user_id: str):
    try:
        logging.info(f"Récupération des groupes de l'utilisateur ID: {user_id}.")
        res = {
                "user": user_id,
                "groups": {
                    element.id: vars(element)
                    for element in bdd_service.get_groups_user(user_id)
                    }
                }
    except DatabaseException as e:
        res = {"error": str(e)}
    return res

@app.get("/group/get_users/{group_id}")
def get_users_in_group(group_id: str):
    try:
        logging.info(f"Récupération des utilisateurs dans le groupe ID: {group_id}.")
        res = {
                "group": group_id,
                "users": [
                    vars(element)
                    for element in bdd_service.get_users_in_group(group_id)
                    ]
                }
    except DatabaseException as e:
        res = {"error": str(e)}
    return res

# User Routes
@app.get("/user/get/{user_id}")
async def get_user(user_id: str):
    try:
        user_or_none = bdd_service.get_user(user_id)
        if (user_or_none == None):
            return {}
        res = {"user": vars(user_or_none)}
    except DatabaseException as e:
        res = {"error": str(e)}
    return res


@app.get("/user/from_auth/{auth_id}")
async def get_user_auth(auth_id: str):
    try:
        user_or_none = bdd_service.get_user_auth(auth_id)
        if (user_or_none == None):
            return {"auth": auth_id}
        res = {
                "auth": auth_id,
                "user": vars(user_or_none)
                }
    except DatabaseException as e:
        res = {"error": str(e)}
    return res


@app.post("/user/new")
def create_user(name: Annotated[str, Body()],
                first_name: Annotated[str, Body()],
                email: Annotated[str, Body()],
                join_date: Annotated[int, Body()],
                auth_id: Annotated[str, Body()],
                ):
    try:
        user = User(
                name,
                first_name,
                email,
                join_date,
                auth_id = auth_id
                )
        user_id = bdd_service.create_user(user)
        res = {"id": user_id, "user": vars(user)}
    except DatabaseException as e:
        res = {"error": str(e)}
    return res

@app.put("/user/modify/{user_id}")
def modify_user(
        user_id: str,
        new_name: Annotated[str, Body()],
        new_first_name: Annotated[str, Body()],
        new_email: Annotated[str, Body()]
        ):
    try:
        bdd_service.set_user(
                user_id,
                User(new_name, new_first_name, new_email, 0, '')
                )
        res = {
                "new_name": new_name,
                "new_first_name": new_first_name,
                "new_email": new_email,
                }
    except DatabaseException as e:
        res = {"error": str(e)}
    return res

@app.delete("/user/delete/{user_id}")
def delete_user(user_id: str):
    try:
        bdd_service.delete_user(user_id)
        res = {"user_deleted": user_id}
    except DatabaseException as e:
        res = {"error": str(e)}
    return res

@app.get("/user/get_by_name/{name}")
def get_by_name(name: str):
    try:
        user_or_none = bdd_service.get_user_name(name)
        res = {"users": [vars(i) for i in user_or_none]}
    except DatabaseException as e:
        res = {"error": str(e)}
    return res

@app.get("/user/get_by_email/{email}")
def get_by_email(email: str):
    try:
        user_or_none = bdd_service.get_user_email(email)
        if (user_or_none == None):
            return {}
        res = {"user": vars(user_or_none)}
    except DatabaseException as e:
        res = {"error": str(e)}
    return res


@app.get("/user/get_all")
def get_all_users():
    try:
        res = {"users": [vars(element) for element in bdd_service.get_all_users()]}
    except DatabaseException as e:
        res = {"error": str(e)}
    return res

# Message Routes

@app.delete("/message/delete/{message_id}")
def delete_message(message_id: str):
    try:
        logging.info(f"Suppression du message ID: {message_id}.")
        bdd_service.delete_message(message_id)
        res = {"message_deleted": message_id}
    except DatabaseException as e:
        res = {"error": str(e)}
    return res


@app.get("/message/get/{message_id}")
def get_message(message_id: str):
    try:
        message_or_none = bdd_service.get_message(message_id)
        if (message_or_none == None):
            return {}
        logging.info(f"Récupération du message ID: {message_id}.")
        res = {"message": vars(message_or_none)}
    except DatabaseException as e:
        res = {"error": str(e)}
    return res

@app.get("/message/get/group/{group_id}")
def get_all_message_group(group_id: str):
    try:
        logging.info(f"Récupération des messages du group {group_id}.")
        res = {"message": [
            vars(message)
            for message in bdd_service.get_all_messages_group(group_id)
            ]}
    except DatabaseException as e:
        res = {"error": str(e)}
    return res

@app.post("/message/create")
def create_message(
        content: Annotated[str, Body()],
        sender_id: Annotated[Union[str, int], Body()],
        receiver_group_id: Annotated[Union[str, int], Body()],
        date: Annotated[int, Body()]
        ):
    try:
        logging.info("Création d'un nouveau message.")
        message = Message(
                content,
                sender_id,
                receiver_group_id,
                date
                )
        message_id = bdd_service.create_message(message)
        res = {"message_id": message_id, "message": vars(message)}
    except DatabaseException as e:
        res = {"error": str(e)}
    return res

@app.get("/media/get/{media_id}")
def get_media(media_id: str):
    try:
        logging.info(f"Récupération du média ID: {media_id}.")
        media_or_none = bdd_service.get_media(media_id)
        if (media_or_none == None):
            return {}
        res = {"media": vars(media_or_none)}
    except DatabaseException as e:
        res = {"error": str(e)}
    return res

@app.get("/media/get_by_message/{message_id}")
def get_media_by_message(message_id: str):
    try:
        logging.info(f"Récupération du média pour le message ID: {message_id}.")
        res = {
                "message_id": message_id,
                "medias": [
                    vars(element)
                    for element in bdd_service.get_medias_message(message_id)
                    ]
                }
    except DatabaseException as e:
        res = {"error": str(e)}
    return res

@app.get("/key/public/get/{group_id}/{user_id}")
def get_public_key(group_id: str, user_id: str):
    try:
        logging.info(
                f"Récupération de la clé public du "
                f"group {group_id} user {user_id}"
                )
        res = {"key": bdd_service.get_public_key(group_id, user_id)}
    except DatabaseException as e:
        res = {"error": str(e)}
    return res

@app.get("/key/private/get/{group_id}/{user_id}")
def get_private_key(group_id: str, user_id: str):
    try:
        logging.info(
                f"Récupération de la clé privée du "
                f"group {group_id} user {user_id}"
                )
        res = {"key": bdd_service.get_private_key(group_id, user_id)}
    except DatabaseException as e:
        res = {"error": str(e)}
    return res

@app.post("/key/private/store/{group_id}/{user_id}")
async def store_private_key(
        group_id: str,
        user_id: str,
        request: Request,
        ):
    try:
        logging.info(
                "Stockage de la clé privée de group {group_id} user {user_id}"
                )
        key = await request.body()
        bdd_service.store_private_key(group_id, user_id, key)
        res = {}
    except DatabaseException as e:
        res = {"error": str(e)}
    return res

@app.post("/key/public/store/{group_id}/{user_id}")
async def store_public_key(
        group_id: str,
        user_id: str,
        request: Request,
        ):
    try:
        logging.info(
                "Stockage de la clé public de group {group_id} user {user_id}"
                )
        key = await request.body()
        bdd_service.store_public_key(group_id, user_id, key)
        res = {}
    except DatabaseException as e:
        res = {"error": str(e)}
    return res

@app.post("/totp/verify")
def verify_totp(
        email: Annotated[str, Body()],
        code: Annotated[str, Body()],
        ):
    try:
        logging.info(
                "Verification de la double authentification pour {email}"
                )
        if auth_service.verify_totp(email, code):
            res = {}
        else:
            res = {"error": "Code not recognized"}
    except DatabaseException as e:
        res = {"error": str(e)}
    return res
