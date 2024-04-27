from typing import Annotated, Any, List

from fastapi import APIRouter, Depends, Request

from stages.exceptions import UserIsNotAdmin
from users.models import User
from users.services import UserService
from .services import RouterService
from .schemas import RouterAdd
from .models import Router

routes_router = APIRouter(tags=["routes"], prefix="/routes")


@routes_router.post("/add")
async def add_route(
    user: Annotated[User, Depends(UserService().get_current_user)], new_route: RouterAdd
) -> Router:
    if not (user.role == "admin"):
        raise UserIsNotAdmin()
    return await RouterService().add_router(new_route)


@routes_router.get("/view")
async def get_region_routes(region: str) -> List[Router]:
    return await RouterService().get_all_region_router(region)


@routes_router.get("")
async def get_route_by_id(route_id: int) -> Router:
    return await RouterService().get_route_by_id(route_id)
