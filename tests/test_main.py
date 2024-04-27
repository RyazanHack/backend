from httpx import AsyncClient

from database import database


async def test_ping(c: AsyncClient):
    response = await c.get("/ping")
    assert response.status_code == 200
    assert response.json() == "pong"


async def test_with_db(c: AsyncClient):
    async with database:
        response = await c.get("/ping")
        assert response.status_code == 200
        assert response.json() == "pong"
