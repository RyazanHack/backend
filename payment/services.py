from config import VOTE_PRICE, DESCRIPTION, HOST
from .repositories import PaymentRepository
from .schemas import PaymentResponse
import uuid
from fastapi import HTTPException
from yookassa import Payment
from .models import Payment as DBPayment


class PaymentService:
    repository = PaymentRepository()

    async def create_payment(self, user_id: int, count_vote: int) -> PaymentResponse:
        amount = count_vote * VOTE_PRICE
        idempotency_key = str(uuid.uuid4())
        return_url = f"{HOST}/payment/{idempotency_key}"
        payment, idempotency_key = create_yookassa_payment(idempotency_key,
                                                           amount, DESCRIPTION,
                                                           return_url
                                                           )

        payment_id = payment.id
        confirmation_url = payment.confirmation.confirmation_url

        await self.repository.create(
            payment_id=payment_id,
            user_id=user_id,
            idempotency_key=idempotency_key,
            votes=count_vote,
        )
        return PaymentResponse(idempotency_key=idempotency_key,
                               confirmation_url=confirmation_url)

    async def set_confirm(self, payment_id: str) -> DBPayment:
        return await self.repository.set_confirm(payment_id)

    async def is_confirmed(self, idempotency_key: str) -> bool:
        payment = await self.repository.get_by_idempotency_key(
            idempotency_key=idempotency_key)
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")

        return payment.confirmed


def create_yookassa_payment(idempotency_key: str, amount: float, description: str,
                            return_url: str):
    payment = Payment.create(
        {
            "amount": {"value": amount, "currency": "RUB"},
            "confirmation": {"type": "redirect", "return_url": return_url},
            "capture": True,
            "description": description,
        },
        idempotency_key,
    )

    return payment, str(idempotency_key)
