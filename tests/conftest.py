import asyncio
from typing import AsyncGenerator

import pytest
import pytest_asyncio
import sqlalchemy
from fastapi.testclient import TestClient
from httpx import AsyncClient

from config import DATABASE_URL
from database import metadata
from main import app


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def c() -> AsyncGenerator[TestClient, None]:
    engine = sqlalchemy.create_engine(DATABASE_URL)
    metadata.create_all(engine)

    httpx_client = AsyncClient(app=app, base_url="http://testserver")

    async with httpx_client as client:
        yield client
    metadata.drop_all(engine)
