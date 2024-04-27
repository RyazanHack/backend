from fastapi import APIRouter

user_router = APIRouter(tags=["user"], prefix="/user")


@user_router.get("/")
async def get_user():
    return {"message": "Hello World"}
