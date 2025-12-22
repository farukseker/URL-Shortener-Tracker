from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, update, delete, func
from sqlalchemy.orm import selectinload
from models import ShortURL, UrlVisitAction, Category
from db import AsyncSessionLocal
from services.shortener import create_short
from security import admin_required


router = APIRouter(
    prefix="/admin/category",
    tags=["admin"],
    dependencies=[Depends(admin_required)],
)

# -------------------------
# Category CRUD
# -------------------------

@router.post("/")
async def create_category(name: str, slug: str):
    async with AsyncSessionLocal() as db:
        existing = await db.execute(select(Category).where(Category.slug == slug))
        if existing.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Slug already exists")
        category = Category(name=name, slug=slug)
        db.add(category)
        await db.commit()
        await db.refresh(category)
        return {"id": category.id, "name": category.name, "slug": category.slug}


@router.get("/")
async def list_categories():
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(Category))
        return [{"id": c.id, "name": c.name, "slug": c.slug} for c in result.scalars().all()]


@router.put("/{category_id}")
async def update_category(category_id: int, name: str | None = None, slug: str | None = None):
    async with AsyncSessionLocal() as db:
        category = await db.get(Category, category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        if name:
            category.name = name
        if slug:
            category.slug = slug
        db.add(category)
        await db.commit()
        return {"status": "updated"}


@router.delete("/{category_id}")
async def delete_category(category_id: int):
    async with AsyncSessionLocal() as db:
        category = await db.get(Category, category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        await db.delete(category)
        await db.commit()
        return {"status": "deleted"}
