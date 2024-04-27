import ormar
from database import BaseMeta


class Router(ormar.Model):
    class Meta(BaseMeta):
        pass

    id: int = ormar.Integer(primary_key=True)
    title: str = ormar.String(max_length=500)
    region: str = ormar.String(max_length=300)
    points = ormar.JSON()
