from typing import Annotated

from fastapi import APIRouter, Header, Depends

from random import randint

from users.models import User
from users.services import UserService

vote_router = APIRouter(tags=["votes"], prefix="/votes")


@vote_router.post('/upvote/{count_vote}')
def upvote(current_user: Annotated[User, Depends(UserService().get_current_user)], count_vote: int):
    return {'success': 'ok'}


@vote_router.get('/{region_name}')
def get_all_votes(current_user: Annotated[User, Depends(UserService().get_current_user)], region_name: str):
    return {'region_name': region_name, 'amount': randint(1, 4445444)}
