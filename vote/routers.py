from fastapi import APIRouter, Header

from random import randint

from users.models import User

votes_router = APIRouter(tags=["votes"], prefix="/votes")


@votes_router.post('/upvote')
def upvote(user: User):
    return {'success': 'ok'}


@votes_router.get('/{region_name}')
def get_all_votes(region_name: str):
    return {'region_name': region_name, 'amount': randint(1, 4445444)}
