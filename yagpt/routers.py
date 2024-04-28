from fastapi import APIRouter
from .services import YAGPTService

yagpt_router = APIRouter(tags=["yagpt"], prefix="/yagpt")


@yagpt_router.get("")
async def get_information(region: str) -> str:
    return await YAGPTService().get_reason(region)
