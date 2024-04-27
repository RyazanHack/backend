from fastapi import APIRouter

vote_router = APIRouter(tags=["vote"], prefix="/vote")


@vote_router.get("")
async def get_vote():
    return {"message": "Fuck you"}
