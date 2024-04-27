from base64 import b64decode
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
# from jose import JWTError
# from jose import jwt, JWTError
from starlette import status
import jwt

from config import SECRET_KEY, ALGORITHM
from utils.passwords import verify_password
from .models import User
from .repositories import UserRepository
from .schemas import TokenData, UserCreate

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class UserService:
    repository = UserRepository()

    async def authenticate_user(self, phone: str, password: str) -> User | None:
        user = await self.repository.get_by_phone(phone)
        if not user:
            return
        if not verify_password(password, user.password_hash):
            return
        return user

    async def authenticate_user_by_token(self, token: str) -> User | None:
        pass

    async def get_current_user(self, token: Annotated[str, Depends(oauth2_scheme)]):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            token = token.strip()
            print(token.strip())

            options = {'verify_aud': False, 'require_sub': True}

            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            print(payload)
            user_id: str = payload.get("sub")
            print(user_id)
            if user_id is None:
                raise credentials_exception
            token_data = TokenData(user_id=user_id)
        except jwt.DecodeError as e:
            print(e)
            raise credentials_exception
        except jwt.ExpiredSignatureError:
            raise credentials_exception
        user = await self.repository.get_by_id(int(token_data.user_id))
        if user is None:
            raise credentials_exception
        return user

    async def create(self, user_create: UserCreate) -> User:
        return await self.repository.create(user_create)
