from typing import Annotated, Any

from fastapi import APIRouter, Depends, Request

from users.models import User
from users.services import UserService
from .schemas import IsConfirmedResponse
from .services import PaymentService

payment_router = APIRouter(tags=["payment"], prefix="/payment")


@payment_router.post("/vote/{count_vote}")
async def payment(
    current_user: Annotated[User, Depends(UserService().get_current_user)],
    count_vote: int,
):
    return await PaymentService().create_payment(
        user_id=current_user.id, count_vote=count_vote
    )


@payment_router.post("/notifications")
async def payment_confirm(request: Request):
    req_json = await request.json()
    print(req_json)

    if req_json["event"] == "payment.succeeded":
        payment_id = req_json["object"]["id"]

        payment = await PaymentService().set_confirm(payment_id)
        await UserService().add_unused_votes(
            user_id=payment.user_id, votes=payment.votes
        )


@payment_router.get("/is_confirmed/{idempotency_key}")
async def payment_confirm(idempotency_key: str) -> IsConfirmedResponse:
    return IsConfirmedResponse(
        is_confirmed=(await PaymentService().is_confirmed(idempotency_key))
    )
