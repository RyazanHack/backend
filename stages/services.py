from vote.models import Vote
from .models import Stage
from .repositories import StageRepository


class StageService:
    def __init__(self) -> None:
        self.repository = StageRepository()

    async def get_current_stage(self) -> Stage:
        return await self.repository.get_current_stage()

    async def set_current_stage(self, stage: int) -> Stage:
        if stage == 2:
            for vote in await Vote.objects.all():
                await vote.update(amount=0)
        return await self.repository.set_current_stage(stage)
