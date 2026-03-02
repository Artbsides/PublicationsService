from fastapi import APIRouter

from app.core.config.environment import settings
from app.modules.uploads.controller import router as uploads_router
from app.modules.publications.controller import router as publications_router


router = APIRouter(
    prefix=settings.APP_PREFIX
)


router.include_router(uploads_router)
router.include_router(publications_router)


@router.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> dict:
    return {"status": "ok"}
