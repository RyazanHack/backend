from typing import List

from .repositories import RouterRepository
from .schemas import RouterAdd
from .models import Router


class RouterService:
    def __init__(self) -> None:
        self.repository = RouterRepository()

    async def add_router(self, new_router: RouterAdd) -> Router:
        return await self.repository.add_router(new_router)

    async def get_all_region_router(self, region: str) -> List[Router]:
        return await self.repository.get_region_routers(region)

    async def get_route_by_id(self, route_id: int) -> Router:
        return await self.repository.get_route_by_id(route_id)

    async def get_all_routes(self) -> List[Router]:
        return await self.repository.get_all_routes()
