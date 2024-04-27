from typing import List

from .models import Router
from .schemas import RouterAdd


class RouterRepository:
    async def add_router(self, new_router: RouterAdd) -> Router:
        return await Router.objects.create(**new_router.dict())

    async def get_region_routers(self, region: str) -> List[Router]:
        return await Router.objects.filter(region=region).all()
