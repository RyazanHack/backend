from pydantic import BaseModel


class UsersRegisteredResponse(BaseModel):
    users_registered: int


class VotesPurchasedResponse(BaseModel):
    votes_purchased: int


class TopRegionResponse(BaseModel):
    regions: dict[str, int]
