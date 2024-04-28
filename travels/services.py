from typing import List

from fastapi import UploadFile

from config import BUCKET_NAME
from s3.api import S3Worker
from users.models import User
from .models import Travel
from .repositories import TravelRepository


class TravelService:
    def __init__(self) -> None:
        self.repository = TravelRepository()

    async def add_travel(self, user: User, route_id: int) -> Travel:
        return await self.repository.add_travel(user, route_id)

    async def get_user_travels(self, user: User) -> List[Travel]:
        return await self.repository.get_user_travels(user)

    async def complete_travel(self, user: User, route_id: int, photo: UploadFile):
        travel = await self.add_travel(user, route_id)
        filename = f"{user.id}_{travel.id}"
        _ = await S3Worker.upload_file(
            bucket=BUCKET_NAME, file=photo, filename=filename
        )
        await self.repository.complete_travel(travel.id, filename)
        travel.update({"path_to_image": filename})
        return travel
