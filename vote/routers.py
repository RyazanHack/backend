from fastapi import APIRouter, Header

from random import randint

from users.models import User

vote_router = APIRouter(tags=["votes"], prefix="/votes")


@vote_router.post('/upvote')
def upvote(user):
    return {'success': 'ok'}


@vote_router.get('/{region_name}')
def get_all_votes(region_name: str):
    return {'region_name': region_name, 'amount': randint(1, 4445444)}
