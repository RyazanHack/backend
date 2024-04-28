from fastapi import APIRouter, HTTPException, Depends
from starlette.responses import FileResponse
from typing_extensions import Annotated

from stages.exceptions import UserIsNotAdmin
from users.models import User
from users.services import UserService
from .services import StatisticService

statistics_router = APIRouter(tags=["statistic"], prefix="/statistic")


@statistics_router.get("/users_registered")
async def users_registered(
        user: Annotated[User, Depends(UserService().get_current_user)]
):
    if not (user.role.value == "admin"):
        raise UserIsNotAdmin()
    return await StatisticService().get_count_users()


@statistics_router.get("/number_purchased_votes")
async def number_purchased_votes(
        user: Annotated[User, Depends(UserService().get_current_user)]
):
    if not (user.role.value == "admin"):
        raise UserIsNotAdmin()
    return await StatisticService().get_votes_purchased()


@statistics_router.get("/top_region/{stage}")
async def top_region(stage: int,
                     user: Annotated[User, Depends(UserService().get_current_user)]
                     ):
    if not (user.role.value == "admin"):
        raise UserIsNotAdmin()
    if stage == 1:
        return await StatisticService().get_top_regions_stage_1()
    elif stage == 2:
        return await StatisticService().get_top_regions_stage_2()
    raise HTTPException(status_code=404, detail="Stage not found")


@statistics_router.get("/xlsx")
async def xlsx(
):
    file_response = FileResponse((await StatisticService().get_xlsx_file()),
                                 filename="statistic.xlsx")
    # background_task.add_task(remove_file, temp_file)
    return file_response
    # return
