from users.services import UserService
from users.models import User
from .repositories import VoteRepository
from .schemas import VoteCreate, RegionResponse, RegionGet
from .exceptions import NotExtraVotes, UserAlreadyVote


class VoteService:
    def __init__(self) -> None:
        self.repository = VoteRepository()

    async def add_vote(self, user: User, vote: VoteCreate) -> None:
        if user.unused_votes <= 0:
            raise NotExtraVotes()
        vote, is_created = await self.repository.add_vote(user, vote)
        if not is_created:
            raise UserAlreadyVote()
        await UserService().subtract_user_voice(user)

    async def get_region_votes(self, searched_region: RegionGet) -> RegionResponse:
        return await self.repository.get_region_votes(searched_region)
