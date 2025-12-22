from fastapi import Header, HTTPException
from config import ADMIN_TOKEN

def admin_required(x_api_key: str = Header(None)):
    if not x_api_key or x_api_key != ADMIN_TOKEN:
        raise HTTPException(status_code=404)
