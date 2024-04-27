from datetime import datetime

from pydantic import BaseModel
from .models import User, Gender


class UserCreate(BaseModel):
    name: str
    surname: str
    phone: str
    gender: Gender
    date_of_birth: str
    email: str
    password: str
    region: str


class UserResponse(User.get_pydantic(
    exclude={'password_hash', 'created_at'})):
    pass


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: str | None = None


class UserLogin(BaseModel):
    phone: str
    password: str
