from .models import Stage


class StageRepository:
    async def get_current_stage(self) -> Stage:
        stage, is_created = await Stage.objects.get_or_create(id=1)
        return stage

    async def set_current_stage(self) -> Stage:
        stage, is_created = await Stage.objects.get_or_create(id=1)
        await stage.update(current_stage=2)
        return stage
