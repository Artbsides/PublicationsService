from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import ValidationError
from fastapi.exceptions import RequestValidationError

from app.lifespan import lifespan
from app.routers.healthcheck import router as healthcheck_router
from app.routers.router import router
from app.core.config.environment import settings
from app.core.exceptions.exception_handler import ExceptionHandler


app = FastAPI(
    lifespan=lifespan, redoc_url=None, docs_url=None if settings.APP_ENVIRONMENT == "production"
        else "/docs", debug=settings.APP_DEBUG
)


app.add_exception_handler(Exception, ExceptionHandler.throw)
app.add_exception_handler(HTTPException, ExceptionHandler.throw)
app.add_exception_handler(RequestValidationError, ExceptionHandler.throw)
app.add_exception_handler(ValidationError, ExceptionHandler.throw)


app.include_router(healthcheck_router)
app.include_router(router)


Instrumentator().instrument(app).expose(
    app, tags=["Monitoring"]
)
