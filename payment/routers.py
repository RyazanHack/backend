from fastapi import APIRouter
from users.models import User

payment_router = APIRouter(tags=["payment"], prefix="/payment")


@payment_router.post("/{count_vote}")
async def payment(user: User, count_vote: int):
    return {'url_for_pay': 'http://localhost:80'}
