from .models import Stage
from .repositories import StageRepository


class StageService:
    def __init__(self) -> None:
        self.repository = StageRepository()

    async def get_current_stage(self) -> Stage:
        return await self.repository.get_current_stage()

    async def set_current_stage(self, stage: int) -> Stage:
        return await self.repository.set_current_stage(stage)
