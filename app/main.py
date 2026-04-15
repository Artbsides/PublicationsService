from fastapi import FastAPI, HTTPException
from pydantic import ValidationError
from fastapi.exceptions import RequestValidationError
from dishka.integrations.fastapi import setup_dishka
from prometheus_fastapi_instrumentator import Instrumentator

from app.router import router
from app.lifespan import lifespan
from app.core.dependencies import build_container
from app.core.config.environment import settings
from app.core.exceptions.exception_handler import ExceptionHandler


app = FastAPI(
    lifespan=lifespan, redoc_url=None, docs_url=None if settings.APP_ENVIRONMENT == "production"
        else "/docs", debug=settings.APP_DEBUG
)


setup_dishka(
    build_container(), app
)


app.add_exception_handler(Exception, ExceptionHandler.throw)
app.add_exception_handler(HTTPException, ExceptionHandler.throw)
app.add_exception_handler(RequestValidationError, ExceptionHandler.throw)
app.add_exception_handler(ValidationError, ExceptionHandler.throw)


app.include_router(router)


Instrumentator().instrument(app).expose(
    app, tags=["Monitoring"], include_in_schema=False
)
