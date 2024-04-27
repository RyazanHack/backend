from typing import Annotated, Any

from fastapi import APIRouter, Depends, Request

from users.models import User
from users.services import UserService
from .services import PaymentService

payment_router = APIRouter(tags=["payment"], prefix="/payment")


@payment_router.post("/vote/{count_vote}")
async def payment(
        current_user: Annotated[User, Depends(UserService().get_current_user)],
        count_vote: int):
    return await PaymentService().create_payment(user_id=current_user.id,
                                           count_vote=count_vote)


@payment_router.post("/notifications")
async def payment_confirm(request: Request):
    print('request')
    req_json = await request.json()

    if req_json["event"] == "payment.succeeded":
        payment_id = req_json["object"]["id"]

        payment = await PaymentService().set_confirm(payment_id)
        await UserService().add_unused_votes(user_id=payment.user_id, votes=payment.votes)
