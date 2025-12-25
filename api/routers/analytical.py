from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, update, delete, func, insert
from sqlalchemy.orm import selectinload
from models import ShortURL, UrlVisitAction, Category, short_url
from models.association import short_url_categories
from db import AsyncSessionLocal
from services.shortener import create_short
from security import admin_required
import schemes as sc
from typing import Optional, Literal, Any

router = APIRouter(
    prefix="/admin/analytical",
    tags=["admin-analytical"],
    dependencies=[Depends(admin_required)],
)

# url-id > visits
# all visits
# delete visits
# mark

@router.get('/list')
async def get_url_visit_actions(url_id: int):
    async with AsyncSessionLocal() as session:
        stmt = (
            select(UrlVisitAction)
            .where(UrlVisitAction.url_id == url_id)
            .order_by(UrlVisitAction.action_at)
        )
        results = await session.execute(stmt)
        if not results:
            raise HTTPException(status_code=404, detail="Not found")
        return results.scalars().all()
