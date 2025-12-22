from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db import AsyncSessionLocal
from services.shortener import create_short

router = APIRouter(prefix="/url")

@router.post("/shorten")
async def shorten(
    long_url: str,
    custom_code: str | None = None,
):
    async with AsyncSessionLocal() as db:
        code = await create_short(db, long_url, custom_code)
        return {"short": f"/r/{code}"}
