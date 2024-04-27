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
        if await User.objects.get_or_none(phone=user_create.phone):
            raise HTTPException(status_code=400,
                                detail="User with this phone already exists")
        password = user_create.password

        dc = user_create.dict(exclude={"password"})
        dc["password_hash"] = get_password_hash(password)
        dc["role"] = Roles.user
        s = datetime.strptime(dc["date_of_birth"], "%d-%m-%Y")
        dc["date_of_birth"] = datetime.date(s)
        user = User(**dc)
        await user.save()

        return user

    async def get_by_email(self, email: str) -> Optional[User]:
        return await User.objects.get_or_none(email=email)

    async def get_by_phone(self, phone: str) -> Optional[User]:
        return await User.objects.get_or_none(phone=phone)

    async def get_by_id(self, user_id: int) -> Optional[User]:
        return await User.objects.get_or_none(id=user_id)

    async def add_unused_votes(self, user_id: int, votes: int) -> User:
        user = await User.objects.get_or_none(id=user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user.unused_votes += votes
        await user.update()
        return user

    async def subtract_user_voice(self, user: User) -> None:
        await user.update(unused_votes=user.unused_votes - 1)
