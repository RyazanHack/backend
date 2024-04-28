import ormar

from users.models import User
from database import BaseMeta


class Vote(ormar.Model):
    class Meta(BaseMeta):
        pass

    id: int = ormar.Integer(primary_key=True)
    user_id: int = ormar.Integer()
    region: str = ormar.String(max_length=255)
    stage: int = ormar.Integer()
    amount: int = ormar.Integer(default=0)


class RegionsStageTwo(ormar.Model):
    class Meta(BaseMeta):
        pass

    id: int = ormar.Integer(primary_key=True)
    region: str = ormar.String(max_length=255)
