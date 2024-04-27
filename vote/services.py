from .repositories import VoteRepository


class VoteService:
    def __init__(self) -> None:
        self.repository = VoteRepository()

