from typing import Annotated

from fastapi import APIRouter, Depends

from users.models import User
from users.services import UserService
from .exceptions import UserIsNotAdmin
from .services import StageService

stage_router = APIRouter(tags=["stage"], prefix="/stage")


@stage_router.get("")
async def get_current_stage():
    return await StageService().get_current_stage()


@stage_router.patch("")
async def set_current_stage(
    user: Annotated[User, Depends(UserService().get_current_user)]
):
    if not (user.role == "admin"):
        raise UserIsNotAdmin()
    return await StageService().set_current_stage()
