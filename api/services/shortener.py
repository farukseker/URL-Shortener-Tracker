from sqlalchemy.ext.asyncio import AsyncSession
from models import ShortURL
from utils import generate_short_code
from cache import url_cache, UrlCacheModel


from sqlalchemy.ext.asyncio import AsyncSession

async def create_short(
    db: AsyncSession,
    long_url: str,
    custom_code: str | None = None,
    preview_type: str | None = None,
) -> ShortURL:
    with db.no_autoflush:
        short = ShortURL(
            long_url=long_url,
            custom=bool(custom_code),
            preview_type=preview_type,
            short_code=custom_code or generate_short_code(),
        )
        db.add(short)

    await db.commit()
    await db.refresh(short)

    url_cache[short.short_code] = UrlCacheModel(
        id=short.id,
        url=long_url,
    )

    return short
