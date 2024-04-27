from pydantic import BaseModel


class PaymentResponse(BaseModel):
    idempotency_key: str
    confirmation_url: str


class IsConfirmedResponse(BaseModel):
    is_confirmed: bool
