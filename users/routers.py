from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette import status

from config import ACCESS_TOKEN_EXPIRE_MINUTES
from users.models import User
from users.schemas import Token, UserLogin, UserCreate, UserResponse
from users.services import UserService
from utils.passwords import create_access_token

user_router = APIRouter(tags=["user"], prefix="/user")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@user_router.get("")
async def get_user():
    return {"message": "Hello World"}


@user_router.post("/register")
async def register(user_create: UserCreate) -> Token:
    user = await UserService().create(user_create)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@user_router.post("/token")
async def login_for_access_token(user_login: UserLogin) -> Token:
    user = await UserService().authenticate_user(user_login.phone, user_login.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@user_router.post("/self")
async def login_for_access_token(
        current_user: Annotated[User, Depends(UserService().get_current_user)],
):
    return UserResponse(**current_user.dict())
