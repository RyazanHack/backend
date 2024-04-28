from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile, File, Query

from s3.api import S3Worker
from users.models import User
from users.services import UserService
from .services import TravelService
from config import BUCKET_NAME

travel_router = APIRouter(tags=["travel"], prefix="/travel")


@travel_router.get("")
async def get_user_travels(
    user: Annotated[User, Depends(UserService().get_current_user)]
):
    return await TravelService().get_user_travels(user)


@travel_router.post("/complete")
async def complete_travel(
    user: Annotated[User, Depends(UserService().get_current_user)],
    travel_id: int = Query(),
    photo: UploadFile = File(None),
):
    return await TravelService().complete_travel(user, travel_id, photo)


@travel_router.get("image/{filename}")
async def get_file_url(filename: str) -> str:
    return await S3Worker.get_file_url(BUCKET_NAME, filename)
