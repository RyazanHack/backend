from typing import List

from config import ALL_REGIONS

from users.models import User
from .exceptions import RegionNotFound
from .models import Vote, RegionsStageTwo
from .schemas import VoteCreate, RegionGet, RegionResponse
from utils.choice_winners import stage_one


class VoteRepository:
    async def add_vote(self, user: User, new_vote: VoteCreate) -> Vote:
        vote, is_created = await Vote.objects.get_or_create(
            **new_vote.dict(exclude={"amount"}), user_id=user.id
        )
        await vote.update(amount=vote.amount + new_vote.amount)
        return vote

    async def add_region_in_two_stage(self, region: str) -> RegionsStageTwo:
        return (await RegionsStageTwo.objects.get_or_create(region=region))[0]

    async def get_region_in_two_stage(self) -> List[RegionsStageTwo]:
        return await RegionsStageTwo.objects.all()

    async def get_region_votes(self, searched_region: RegionGet) -> RegionResponse:
        votes = await Vote.objects.filter(
            region=searched_region.region, stage=searched_region.stage
        ).sum("amount")
        if not votes:
            raise RegionNotFound(searched_region.region)
        return RegionResponse(votes=votes, **searched_region.dict())

    async def stage_one(self):
        votes = await Vote.objects.filter(stage=1).all()
        new_regions = ALL_REGIONS.copy()
        for vote in votes:
            new_regions[vote.region] += vote.amount
        all_regions, result = stage_one(
            sorted(new_regions.items(), key=lambda x: x[1], reverse=True)
        )
        for region in all_regions:
            await self.add_region_in_two_stage(region)
        return result

    async def stage_two(self):
        votes = await Vote.objects.filter(stage=2).all()
        winner_regions = await self.get_region_in_two_stage()
        winner_regions_dict = {region.region: 0 for region in winner_regions}
        for vote in votes:
            winner_regions_dict[vote.region] += vote.amount
        winner_regions_dict = sorted(
            winner_regions_dict.items(), key=lambda x: x[1], reverse=True
        )
        return winner_regions_dict[:10]
