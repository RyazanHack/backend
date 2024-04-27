from fastapi import HTTPException, status


class UserIsNotAdmin(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not a admin",
        )
