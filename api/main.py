from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlalchemy import select

from db import AsyncSessionLocal, engine
from models import ShortURL
from cache import url_cache
from db_init import init_db

from routers.redirect import router as redirect_router
# from routers.shorten import router as shorten_router
from routers.admin import router as admin_router
from routers.category import router as category_router

from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await init_db(engine)

        async with AsyncSessionLocal() as db:
            result = await db.execute(
                select(ShortURL.short_code, ShortURL.long_url)
            )
            for code, url in result.all():
                url_cache[code] = url
    except Exception as e:
        print("Startup skipped:", e)
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(redirect_router)
# app.include_router(shorten_router)
app.include_router(admin_router)
app.include_router(category_router)



