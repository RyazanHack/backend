import datetime
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
    phone: str = ormar.String(max_length=200)
    phone_verified: bool = ormar.Boolean(default=False)
    role: Roles = ormar.Enum(enum_class=Roles)
    gender: Gender = ormar.Enum(enum_class=Gender)
    date_of_birth: datetime.date = ormar.Date()
    password_hash: str = ormar.String(max_length=200)
    created_at: datetime.datetime = ormar.DateTime(default=datetime.datetime.now)
    region: str = ormar.String(max_length=255)
    unused_votes: int = ormar.Integer(default=0)
