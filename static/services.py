from config import ALL_REGIONS
from payment.repositories import PaymentRepository
from users.repositories import UserRepository
from vote.models import Vote
from vote.repositories import VoteRepository
from .schemas import UsersRegisteredResponse, VotesPurchasedResponse


class StatisticService:
    user_repository = UserRepository()
    vote_repository = VoteRepository()
    payment_repository = PaymentRepository()

    async def get_count_users(self) -> UsersRegisteredResponse:
        count_users = await self.user_repository.count()
        return UsersRegisteredResponse(users_registered=count_users)

    async def get_votes_purchased(self) -> VotesPurchasedResponse:
        votes_purchased = 0
        for payment in await self.payment_repository.get_all():
            if payment.confirmed:
                votes_purchased += payment.votes
        return VotesPurchasedResponse(votes_purchased=votes_purchased)

    async def get_top_regions_stage_2(self):
        votes = await Vote.objects.filter(stage=2).all()
        winner_regions = await self.vote_repository.get_region_in_two_stage()
        winner_regions_dict = {region.region: 0 for region in winner_regions}
        for vote in votes:
            winner_regions_dict[vote.region] += vote.amount
        winner_regions_dict = sorted(
            winner_regions_dict.items(), key=lambda x: x[1], reverse=True
        )
        return winner_regions_dict[:10]

    async def get_top_regions_stage_1(self):
        votes = await Vote.objects.filter(stage=1).all()
        winner_regions_dict = {region: 0 for region in ALL_REGIONS.keys()}
        for vote in votes:
            winner_regions_dict[vote.region] += vote.amount
        winner_regions_dict = sorted(
            winner_regions_dict.items(), key=lambda x: x[1], reverse=True
        )
        return winner_regions_dict[:10]
