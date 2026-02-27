from fastapi import FastAPI

from app.confs.settings import settings


app = FastAPI(
    redoc_url=None, docs_url=None if settings.APP_ENVIRONMENT == "production"
        else "/docs", debug=settings.APP_DEBUG
)
