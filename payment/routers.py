from typing import Annotated, Any

from fastapi import APIRouter, Depends, Request

from users.models import User
from users.services import UserService
from .services import create_payment

payment_router = APIRouter(tags=["payment"], prefix="/payment")


@payment_router.post("/payment/{count_vote}")
async def payment(
        current_user: Annotated[User, Depends(UserService().get_current_user)],
        count_vote: int):
    return create_payment(100, "test", "http://localhost:8000/docs")


@payment_router.post("/notifications")
async def payment_confirm(request: Request):
    print('request')
    return Request
