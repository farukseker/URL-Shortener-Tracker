from sqlalchemy import (
    String,
    Boolean,
    DateTime,
    func,
    UniqueConstraint,
    Enum,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from .enums import PreviewType
from .association import short_url_categories


class ShortURL(Base):
    __tablename__ = "short_urls"
    __table_args__ = (UniqueConstraint("short_code"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    short_code: Mapped[str] = mapped_column(String(16), index=True)
    long_url: Mapped[str] = mapped_column(String, nullable=False)

    custom: Mapped[bool] = mapped_column(Boolean, default=False)

    preview_type: Mapped[PreviewType] = mapped_column(
        Enum(PreviewType, name="preview_type_enum"),
        default=PreviewType.url,
        nullable=False,
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    categories: Mapped[list["Category"]] = relationship(
        "Category",
        secondary=short_url_categories,
        back_populates="urls",
        lazy="selectin"

    )
