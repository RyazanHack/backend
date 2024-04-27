import datetime

import ormar

from database import BaseMeta


class Payment(ormar.Model):
    class Meta(BaseMeta):
        pass

    id: int = ormar.Integer(primary_key=True)
    user_id: int = ormar.Integer()
    votes: int = ormar.Integer(default=0)
    payment_id: str = ormar.String(max_length=300)
    idempotency_key: str = ormar.String(max_length=300)
    confirmed: bool = ormar.Boolean(default=False)
    created_at: str = ormar.DateTime(default=datetime.datetime.now)
