from typing import Annotated

from fastapi import APIRouter, Header, Depends

from random import randint

from .models import Vote
from .services import VoteService
from .schemas import VoteCreate, RegionGet, RegionResponse

from users.models import User
from users.services import UserService

vote_router = APIRouter(tags=["votes"], prefix="/votes")


@vote_router.post("/upvote")
async def upvote(
    current_user: Annotated[User, Depends(UserService().get_current_user)],
    vote: VoteCreate,
) -> Vote:
    return await VoteService().add_vote(current_user, vote)


@vote_router.post("")
async def get_region_votes(
    searched_region: RegionGet,
) -> RegionResponse:
    return await VoteService().get_region_votes(searched_region)


@vote_router.get("/stage_one")
async def get_region_in_one_stage():
    return await VoteService().get_winner_stage_one()


@vote_router.get("/stage_two")
async def get_region_in_two_stage():
    return await VoteService().get_winner_stage_two()
