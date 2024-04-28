from typing import List

from config import ALL_REGIONS

from users.models import User
from .exceptions import RegionNotFound
from .models import Vote, RegionsStageTwo
from .schemas import VoteCreate, RegionGet, RegionResponse
from utils.choice_winners import stage_one
from stages.services import StageService


class VoteRepository:
    async def add_vote(self, user: User, new_vote: VoteCreate) -> Vote:
        vote, is_created = await Vote.objects.get_or_create(
            **new_vote.dict(exclude={"amount"}), user_id=user.id
        )
        await vote.update(amount=vote.amount + new_vote.amount)
        if (await StageService().get_current_stage()).current_stage == 2:
            new_vote.stage = 1
            vote_new_stage, is_created = await Vote.objects.get_or_create(
                **new_vote.dict(exclude={"amount"}), user_id=user.id
            )

            await vote_new_stage.update(amount=vote_new_stage.amount + new_vote.amount)
            # print(vote, vote_new_stage)
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
            return RegionResponse(votes=0, **searched_region.dict())
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

    async def reset_amount(self):
        for vote in await Vote.objects.all():
            await vote.update(each=True, amount=0)
