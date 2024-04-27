from datetime import datetime
from typing import Optional

from utils.passwords import get_password_hash
from .models import User, Roles
from .schemas import UserCreate

from fastapi import HTTPException


class UserRepository:
    """
    UserRepository
    """

    async def create(self, user_create: UserCreate) -> User:

        u = await User.objects.get_or_none(phone=user_create.phone)
        print(u)



        if u:
            raise HTTPException(status_code=400, detail="User with this phone already exists")

        password = user_create.password
        # user_dict = user_create.dict()
        # del user_dict["password"]
        # print(user_dict)
        dc = user_create.dict(exclude={"password"})
        dc["password_hash"] = get_password_hash(password)
        dc["role"] = Roles.user
        s = datetime.strptime(dc["date_of_birth"], "%d-%m-%Y")
        dc["date_of_birth"] = datetime.date(s)
              # "password_hash": get_password_hash(password)}}
        user = User(**dc)

        # user.password_hash = get_password_hash(password)
        await user.save()
        return user

    async def get_by_email(self, email: str):
        return await User.objects.get_or_none(email=email)

    async def get_by_phone(self, phone: str):
        return await User.objects.get_or_none(phone=phone)

    async def get_by_id(self, user_id: int) -> Optional[User]:
        return await User.objects.get_or_none(id=user_id)
