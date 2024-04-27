from fastapi import APIRouter

payment_router = APIRouter(tags=["payment"], prefix="/payment")


@payment_router.get("")
async def get_payment():
    return {"message": "Fuck you"}
