from sqlalchemy import (
    String,
    DateTime,
    func,
    UniqueConstraint,
    Integer,
    Index,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class UrlVisitAction(Base):
    __tablename__ = "url_visit_actions"
    __table_args__ = (
        UniqueConstraint("url", "ip_address", name="uq_url_ip"),
        Index("ix_visit_country", "country"),
        Index("ix_visit_city", "city"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String, index=True, nullable=False)
    ip_address: Mapped[str] = mapped_column(String(45), nullable=False)

    ip_host: Mapped[str | None] = mapped_column(String)
    ip_provider: Mapped[str | None] = mapped_column(String)

    country: Mapped[str | None] = mapped_column(String)
    city: Mapped[str | None] = mapped_column(String)

    geo_data: Mapped[dict | None] = mapped_column(JSONB)

    user_agent: Mapped[str] = mapped_column(String, nullable=False)
    count: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    action_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
