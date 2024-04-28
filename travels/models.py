from typing import Optional

import ormar

from database import BaseMeta


class Travel(ormar.Model):
    class Meta(BaseMeta):
        pass

    id: int = ormar.Integer(primary_key=True)
    user_id: int = ormar.Integer()
    route_id: int = ormar.Integer()
    path_to_image: str = ormar.String(max_length=500, default="")
