from typing import List

from .models import Router
from .schemas import RouterAdd
from .exceptions import RouteNotFound


class RouterRepository:
    async def add_router(self, new_router: RouterAdd) -> Router:
        return await Router.objects.create(**new_router.dict())

    async def get_region_routers(self, region: str) -> List[Router]:
        return await Router.objects.filter(region=region).all()

    async def get_route_by_id(self, route_id: int) -> Router:
        route = await Router.objects.get_or_none(id=route_id)
        if not route:
            raise RouteNotFound()
        return route

    async def get_all_routes(self) -> List[Router]:
        return await Router.objects.all()
