from config import VOTE_PRICE, DESCRIPTION, RETURN_URL
from .repositories import PaymentRepository
from .schemas import PaymentResponse
import uuid

from yookassa import Payment
from .models import Payment as DBPayment


class PaymentService:
    repository = PaymentRepository()

    async def create_payment(self, user_id: int, count_vote: int) -> PaymentResponse:
        amount = count_vote * VOTE_PRICE
        payment, idempotency_key = create_yookassa_payment(
            amount, DESCRIPTION, RETURN_URL
        )

        payment_id = payment.id
        confirmation_url = payment.confirmation.confirmation_url

        await self.repository.create(
            payment_id=payment_id,
            user_id=user_id,
            idempotency_key=idempotency_key,
            votes=count_vote,
        )
        return PaymentResponse(confirmation_url=confirmation_url)

    async def set_confirm(self, payment_id: str) -> DBPayment:
        return await self.repository.set_confirm(payment_id)


def create_yookassa_payment(amount: float, description: str, return_url: str):
    idempotency_key = uuid.uuid4()
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
