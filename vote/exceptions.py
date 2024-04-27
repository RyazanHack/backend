from fastapi import HTTPException, status


class NotExtraVotes(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not extra votes",
        )


class UserAlreadyVote(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user has already voted for this region at this stage",
        )


class RegionNotFound(HTTPException):
    def __init__(self, region: str) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Region {region} not found"
        )
