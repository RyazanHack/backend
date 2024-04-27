from pydantic import BaseModel


class VoteCreate(BaseModel):
    region: str
    stage: int
    amount: int


class RegionGet(BaseModel):
    region: str
    stage: int


class RegionResponse(BaseModel):
    region: str
    stage: int
    votes: int
