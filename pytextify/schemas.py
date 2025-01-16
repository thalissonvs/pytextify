from typing import Optional

from pydantic import BaseModel, EmailStr


class ImageSchema(BaseModel):
    image_base64: str


class TaskSchema(BaseModel):
    task_id: str
    status: str
    credits: int


class TaskResultSchema(TaskSchema):
    result: Optional[list] = None


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr


class UserList(BaseModel):
    users: list[UserPublic]


class Token(BaseModel):
    access_token: str
    token_type: str
