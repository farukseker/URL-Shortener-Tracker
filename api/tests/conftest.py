import sys
from pathlib import Path
import os
import pytest_asyncio
from httpx import AsyncClient
from httpx import ASGITransport

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

os.environ["ADMIN_TOKEN"] = "test-admin-token"
os.environ["DATABASE_URL"] = "postgresql+asyncpg://postgres:postgres@localhost:5432/urlshort_test"

from main import app


@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as ac:
        yield ac
