from sqlalchemy import String, DateTime, func, UniqueConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from .association import short_url_categories


class Category(Base):
    __tablename__ = "categories"
    __table_args__ = (
        UniqueConstraint("slug", name="uq_category_slug"),
        Index("ix_category_name", "name"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    slug: Mapped[str] = mapped_column(String(64), nullable=False)

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    urls: Mapped[list["ShortURL"]] = relationship(
        secondary=short_url_categories,
        back_populates="categories",
    )
