from users.services import UserService
from users.models import User
from .models import Vote
from .repositories import VoteRepository
from .schemas import VoteCreate, RegionResponse, RegionGet
from .exceptions import NotExtraVotes, UserAlreadyVote


class VoteService:
    def __init__(self) -> None:
        self.repository = VoteRepository()

    async def add_vote(self, user: User, vote: VoteCreate) -> Vote:
        if user.unused_votes < vote.amount:
            raise NotExtraVotes()
        vote = await self.repository.add_vote(user, vote)
        await UserService().subtract_user_voice(user, vote.amount)
        return vote

    async def get_region_votes(self, searched_region: RegionGet) -> RegionResponse:
        return await self.repository.get_region_votes(searched_region)
