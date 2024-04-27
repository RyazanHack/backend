from pydantic import BaseModel, Json


class RouterAdd(BaseModel):
    title: str
    region: str
    points: Json
