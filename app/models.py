import datetime
from typing import List

from pydantic import BaseModel


class User(BaseModel):
    def __init__(self, user_id: int, username: str, name: str, email: str, join_date: datetime, auth_id: int, hashed_password: str):
        self.id = user_id
        self.username = username
        self.name = name
        self.email = email
        self.join_date = join_date
        self.auth_id = auth_id
        self.password = hashed_password


class Group:
    def __init__(self, group_id: int, name: str, users: List[User] = None):
        self.id = group_id
        self.name = name
        self.users = users


class UserInGroup:
    def __init__(self, id: int, user_id: int, group_id: int):
        self.id = id
        self.user_id = user_id
        self.group_id = group_id


class Message(BaseModel):
    def __init__(self, message_id: int, text: str, sender_id: int, receiver_group_id: int, date: datetime):
        self.id = message_id
        self.content = text
        self.sender_id = sender_id
        self.receiver_group_id = receiver_group_id
        self.date = date


class Media(BaseModel):
    def __int__(self, id: int, type: str, link: str, message_id: int):
        self.id = id
        self.type = type
        self.link = link
        self.message_id = message_id
