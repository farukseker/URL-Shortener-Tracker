from sqlalchemy.ext.asyncio import AsyncSession
from models import ShortURL
from utils import generate_short_code
from cache import url_cache


async def create_short(db, long_url, custom_code=None, preview_type=None) -> ShortURL:
    short = ShortURL(
        long_url=long_url,
        custom=bool(custom_code),
        preview_type=preview_type,
        short_code=custom_code or generate_short_code(),
    )
    db.add(short)
    url_cache[short.short_code] = long_url
    return short
