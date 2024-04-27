from typing import Annotated

from fastapi import APIRouter, Depends
from users.models import User
from users.services import UserService

payment_router = APIRouter(tags=["payment"], prefix="/payment")


@payment_router.post("/{count_vote}")
async def payment(current_user: Annotated[User, Depends(UserService().get_current_user)], count_vote: int):
    return {'url_for_pay': 'http://localhost:80'}
