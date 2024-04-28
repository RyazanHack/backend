from typing import List

from users.services import UserService
from users.models import User
from .models import Vote, RegionsStageTwo
from .repositories import VoteRepository
from .schemas import VoteCreate, RegionResponse, RegionGet
from .exceptions import NotExtraVotes, UserAlreadyVote


class VoteService:
    def __init__(self) -> None:
        self.repository = VoteRepository()

    async def add_vote(self, user: User, new_vote: VoteCreate) -> Vote:
        if user.unused_votes < new_vote.amount:
            raise NotExtraVotes()
        vote = await self.repository.add_vote(user, new_vote)
        await UserService().subtract_user_voice(user, new_vote.amount)
        return vote

    async def get_region_votes(self, searched_region: RegionGet) -> RegionResponse:
        return await self.repository.get_region_votes(searched_region)

    async def get_winner_stage_one(self):
        return await self.repository.stage_one()

    async def get_winner_stage_two(self):
        return await self.repository.stage_two()

    async def reset_amount(self):
        return await self.repository.reset_amount()

    async def get_region_in_two_stage(self) -> List[RegionsStageTwo]:
        return await RegionsStageTwo.objects.all()
