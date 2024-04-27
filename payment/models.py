from vote.models import Vote

import ormar

from database import BaseMeta


class Payment(ormar.Model):
    class Meta(BaseMeta):
        pass

    id: int = ormar.Integer(primary_key=True)
    vote_id: Vote = ormar.ForeignKey(Vote)
    payment_id: str = ormar.String(max_length=300)
    idempotency_key: str = ormar.String(max_length=300)
    confirmed: bool = ormar.Boolean(default=False)
    created_at: str = ormar.DateTime(default=ormar.DateTime.now)
