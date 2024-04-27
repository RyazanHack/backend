from enum import Enum

import ormar

from database import BaseMeta


class Roles(Enum):
    user = "user"
    admin = "admin"


class Gender(Enum):
    male = "male"
    female = "female"


class User(ormar.Model):
    class Meta(BaseMeta):
        pass

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=200)
    surname: str = ormar.String(max_length=200)
    patronymic: str = ormar.String(max_length=200)
    phone: str = ormar.String(max_length=200)
    phone_verificated: bool = ormar.Boolean(default=False)
    role: Roles = ormar.Enum(enum_class=Roles)
    gender: Gender = ormar.Enum(enum_class=Gender)
    date_of_birth: str = ormar.Date()
    email: str = ormar.String(max_length=200)
    email_verified: bool = ormar.Boolean(default=False)
    password_hash: str = ormar.String(max_length=200)
    created_at: str = ormar.DateTime(default=ormar.DateTime.now)

