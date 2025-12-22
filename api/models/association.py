from sqlalchemy import Table, Column, ForeignKey
from .base import Base


short_url_categories = Table(
    "short_url_categories",
    Base.metadata,
    Column(
        "short_url_id",
        ForeignKey("short_urls.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "category_id",
        ForeignKey("categories.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)
