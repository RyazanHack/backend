from pydantic import BaseModel


class PaymentResponse(BaseModel):
    confirmation_url: str
