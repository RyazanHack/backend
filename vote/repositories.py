from users.models import User
from .models import Vote
from .schemas import VoteCreate, RegionGet, RegionResponse


class VoteRepository:
    async def add_vote(self, user: User, vote: VoteCreate) -> Vote:
        return await Vote.objects.get_or_create(**vote.dict(), user_id=user.id)

    async def get_region_votes(self, searched_region: RegionGet) -> RegionResponse:
        votes = await Vote.objects.filter(
            region=searched_region.region, stage=searched_region.stage
        ).all()
        return RegionResponse(votes=len(votes), **searched_region.dict())
