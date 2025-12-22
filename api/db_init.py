
from sqlalchemy.ext.asyncio import AsyncEngine
from db import engine, engine
from models import Base

async def init_db(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == '__main__':
    import asyncio
    asyncio.run(init_db(engine))
