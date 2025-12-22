from pydantic import BaseModel


class ShortCreate(BaseModel):
    long_url: str
    preview_type: str | None = None
    custom_code: str | None = None
    category_ids: list[int] = []
