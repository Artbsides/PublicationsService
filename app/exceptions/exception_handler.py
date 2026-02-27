import importlib
from fastapi.encoders import jsonable_encoder
import inflection

from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException

from app.exceptions.errors.base import BaseError
from app.exceptions.errors.internal_server_error import InternalServerError


class ExceptionHandler:
    @staticmethod
    def throw(_: Request, exception: BaseError) -> JSONResponse:
        module = "HTTPExceptionError" if isinstance(exception, HTTPException) \
            else type(exception).__name__

        try:
            exception = getattr(importlib.import_module(
                f"app.exceptions.errors.{ inflection.underscore(module).replace("_error", "") }"), module)(exception)
        except:
            exception = InternalServerError

        response = {
            "data": exception.args
        }

        return JSONResponse(
            jsonable_encoder(response), getattr(exception, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
        )
