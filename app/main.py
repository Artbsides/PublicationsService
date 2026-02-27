from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError

from app.confs.lifespan import lifespan
from app.confs.environment import settings
from app.exceptions.exception_handler import ExceptionHandler
from app.routers.router import router


app = FastAPI(
    lifespan=lifespan, redoc_url=None, docs_url=None if settings.APP_ENVIRONMENT == "production"
        else "/docs", debug=settings.APP_DEBUG
)


app.add_exception_handler(Exception, ExceptionHandler.throw)
app.add_exception_handler(HTTPException, ExceptionHandler.throw)
app.add_exception_handler(RequestValidationError, ExceptionHandler.throw)


app.include_router(router)
