import ormar

from database import BaseMeta


class Stage(ormar.Model):
    class Meta(BaseMeta):
        pass

    id: int = ormar.Integer(primary_key=True)
    current_stage: int = ormar.Integer(default=1)
