from typing import List

from users.models import User
from .models import Travel
from .exceptions import TravelNotFound


class TravelRepository:
    async def add_travel(self, user: User, route_id: int) -> Travel:
        return await Travel.objects.create(user_id=user.id, route_id=route_id)

    async def get_user_travels(self, user: User) -> List[Travel]:
        return await Travel.objects.filter(user_id=user.id).all()

    async def complete_travel(self, travel_id: int, path_to_image: str) -> Travel:
        travel = await Travel.objects.get_or_none(id=travel_id)
        if not travel:
            raise TravelNotFound()
        await travel.update(path_to_image=path_to_image)
        return travel
