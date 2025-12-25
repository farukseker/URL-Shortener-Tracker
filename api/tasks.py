from sqlalchemy import func
from sqlalchemy.dialects.postgresql import insert
from db import AsyncSessionLocal
from models import UrlVisitAction
from utils import get_client_ip, get_ip_data
from fastapi import Request
from config import BOT_UA_REGEX


async def save_url_action(
    request,
    url_id: int,
    user_agent: str,
    skip_analytics: bool = False,
):
    if skip_analytics:
        return

    ip = get_client_ip(request)
    ip_data = await get_ip_data(ip)

    stmt = insert(UrlVisitAction).values(
        url_id=url_id,
        ip_address=ip,
        ip_host=ip_data.get("host"),
        ip_provider=ip_data.get("provider"),
        country=ip_data.get("country"),
        city=ip_data.get("city"),
        geo_data=ip_data,
        user_agent=user_agent,
        count=1,
    ).on_conflict_do_update(
        constraint="uq_url_ip",
        set_={
            "count": UrlVisitAction.count + 1,
            "action_at": func.now(),
        },
    )

    async with AsyncSessionLocal() as session:
        await session.execute(stmt)
        await session.commit()


def is_bot_ua(request: Request) -> bool:
    ua = request.headers.get("user-agent", "")
    return bool(BOT_UA_REGEX.search(ua))
