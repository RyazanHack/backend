import ormar

from users.models import User
from database import BaseMeta


class Vote(ormar.Model):
    class Meta(BaseMeta):
        pass

    id: int = ormar.Integer(primary_key=True)
    user_id: User = ormar.ForeignKey(User)
    region: str = ormar.String(max_length=255)
    amount: int = ormar.Integer()
    stage: int = ormar.Integer()
