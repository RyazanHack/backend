from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile, File, Query

from users.models import User
from users.services import UserService
from .services import TravelService

travel_router = APIRouter(tags=["travel"], prefix="/travel")


@travel_router.post("")
async def add_user_travel(
    user: Annotated[User, Depends(UserService().get_current_user)], route_id: int
):
    return await TravelService().add_travel(user, route_id)


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
