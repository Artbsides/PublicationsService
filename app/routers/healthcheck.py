from fastapi import APIRouter
from fastapi.responses import JSONResponse


router = APIRouter()


@router.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> JSONResponse:
    return JSONResponse({"status": "ok"})
