from users.models import User
from .models import Vote
from .schemas import VoteCreate, RegionGet, RegionResponse


class VoteRepository:
    async def add_vote(self, user: User, new_vote: VoteCreate) -> Vote:
        vote, is_created = await Vote.objects.get_or_create(
            **new_vote.dict(exclude={"amount"}), user_id=user.id
        )
        await vote.update(amount=vote.amount + new_vote.amount)
        return vote

    async def get_region_votes(self, searched_region: RegionGet) -> RegionResponse:
        votes = await Vote.objects.filter(
            region=searched_region.region, stage=searched_region.stage
        ).sum("amount")
        return RegionResponse(votes=votes, **searched_region.dict())
