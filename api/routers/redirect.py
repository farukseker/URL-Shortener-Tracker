from fastapi import APIRouter, HTTPException, Request, BackgroundTasks
from fastapi.responses import RedirectResponse
from cache import url_cache, UrlCacheModel
from tasks import save_url_action, is_bot_ua

router = APIRouter()

@router.get("/r/{code}")
def redirect(
    code: str,
    request: Request,
    background_tasks: BackgroundTasks,
):
    url: UrlCacheModel | None = url_cache.get(code)
    if not url:
        raise HTTPException(status_code=404)
    background_tasks.add_task(
        save_url_action,
        request,
        url.id,
        request.headers.get("user-agent", ""),
        skip_analytics=is_bot_ua(request),
    )

    return RedirectResponse(url.url)
