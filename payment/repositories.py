from .models import Payment


class PaymentRepository:
    async def create(self, payment_id: str, user_id: int, idempotency_key: str,
                     votes: int):
        payment = Payment(
            payment_id=payment_id,
            user_id=user_id,
            idempotency_key=idempotency_key,
            votes=votes
        )
        await payment.save()
        return payment

    async def set_confirm(self, payment_id) -> Payment:
        payment = await Payment.objects.get(payment_id=payment_id)
        payment.confirmed = True
        await payment.update()
        return payment
