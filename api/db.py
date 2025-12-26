from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from config import DATABASE_URL


# DATABASE_URL = 'postgresql+asyncpg://postgres:postgres@localhost:1000/urlshort'

engine = create_async_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

class Base(DeclarativeBase):
    pass
