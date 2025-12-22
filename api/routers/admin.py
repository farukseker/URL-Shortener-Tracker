from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, update, delete, func, insert
from sqlalchemy.orm import selectinload
from models import ShortURL, UrlVisitAction, Category
from models.association import short_url_categories
from db import AsyncSessionLocal
from services.shortener import create_short
from security import admin_required
import schemes as sc 

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(admin_required)],
)

# -------------------------
# ShortURL CRUD
# -------------------------

@router.post("/create")
async def create_short_url(payload: sc.ShortCreate):
    async with AsyncSessionLocal() as db:
        try:
            short = await create_short(
                db=db,
                long_url=payload.long_url,
                custom_code=payload.custom_code,
                preview_type=payload.preview_type,
            )

            await db.flush()  # short.id guaranteed

            if payload.category_ids:
                values = [
                    {
                        "short_url_id": short.id,
                        "category_id": cid,
                    }
                    for cid in payload.category_ids
                ]

                await db.execute(
                    insert(short_url_categories).values(values)
                )

            await db.commit()

            return {
                "short": f"/r/{short.short_code}",
                "code": short.short_code,
            }

        except Exception:
            await db.rollback()
            raise


@router.get("/list")
async def list_short_urls():
    async with AsyncSessionLocal() as db:
        stmt = (
            select(
                ShortURL.short_code,
                ShortURL.long_url,
                ShortURL.custom,
                ShortURL.preview_type,
                ShortURL.created_at,
                func.coalesce(func.sum(UrlVisitAction.count), 0).label("click_count"),
            )
            .outerjoin(
                UrlVisitAction,
                UrlVisitAction.url == ShortURL.short_code,
            )
            .group_by(
                ShortURL.short_code,
                ShortURL.long_url,
                ShortURL.custom,
                ShortURL.preview_type,
                ShortURL.created_at,
            )
        )
        result = await db.execute(stmt)
        return [
            {
                "code": code,
                "url": url,
                "custom": custom,
                "preview_type": preview_type,
                "created_at": created_at,
                "click_count": click_count,
            }
            for code, url, custom, preview_type, created_at, click_count in result.all()
        ]


@router.get("/url")
async def get_short_url(code: str):
    async with AsyncSessionLocal() as db:
        stmt = (
            select(ShortURL)
            .where(ShortURL.short_code == code)
            .options(selectinload(ShortURL.categories))
        )
        result = await db.execute(stmt)
        short = result.scalar_one_or_none()

        if not short:
            raise HTTPException(status_code=404, detail="Not found")

        return {
            "code": short.short_code,
            "url": short.long_url,
            "custom": short.custom,
            "created_at": short.created_at,
            "categories": [{"id": c.id, "name": c.name} for c in short.categories]
        }


@router.put("/url")
async def update_short_url(
    code: str,
    long_url: str,
    category_ids: list[int] | None = None
):
    async with AsyncSessionLocal() as db:
        stmt = (
            select(ShortURL)
            .where(ShortURL.short_code == code)
            .options(selectinload(ShortURL.categories))
        )
        short = (await db.execute(stmt)).scalar_one_or_none()
        if not short:
            raise HTTPException(status_code=404, detail="Not found")

        short.long_url = long_url

        if category_ids is not None:
            result = await db.execute(select(Category).where(Category.id.in_(category_ids)))
            short.categories = result.scalars().all()

        db.add(short)
        await db.commit()
        return {"status": "updated"}


@router.delete("/url")
async def delete_short_url(code: str):
    async with AsyncSessionLocal() as db:
        stmt = select(ShortURL).where(ShortURL.short_code == code)
        short = (await db.execute(stmt)).scalar_one_or_none()
        if not short:
            raise HTTPException(status_code=404, detail="Not found")
        await db.delete(short)
        await db.commit()
        return {"status": "deleted"}

