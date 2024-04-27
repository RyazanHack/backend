from .repositories import PaymentRepository


class PaymentService:
    def __init__(self) -> None:
        self.repository = PaymentRepository()
