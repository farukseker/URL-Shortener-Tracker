import json
from datetime import timedelta
from sqlalchemy import select, update
from sqlalchemy.sql import func
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

    async with AsyncSessionLocal() as session:
        one_hour_ago = func.now() - timedelta(hours=1)

        stmt = (
            select(UrlVisitAction)
            .where(
                UrlVisitAction.url_id == url_id,
                UrlVisitAction.ip_address == ip,
                UrlVisitAction.action_at >= one_hour_ago,
            )
            .order_by(UrlVisitAction.action_at.desc())
            .limit(1)
        )

        result = await session.execute(stmt)
        action = result.scalar_one_or_none()

        if action:
            await session.execute(
                update(UrlVisitAction)
                .where(UrlVisitAction.id == action.id)
                .values(
                    count=UrlVisitAction.count + 1,
                    action_at=func.now(),
                )
            )
        else:
            session.add(
                UrlVisitAction(
                    url_id=url_id,
                    ip_address=ip,
                    ip_host=ip_data.get("host"),
                    ip_provider=ip_data.get("isp"),
                    country=ip_data.get("country"),
                    city=ip_data.get("city"),
                    geo_data=ip_data,
                    user_agent=user_agent,
                    count=1,
                )
            )

        await session.commit()


def is_bot_ua(request: Request) -> bool:
    ua = request.headers.get("user-agent", "")
    return bool(BOT_UA_REGEX.search(ua))
