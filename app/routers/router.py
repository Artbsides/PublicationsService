from fastapi import Depends, APIRouter

from app.core.authorization import Authorization
from app.core.config.environment import settings


router = APIRouter(
    prefix=settings.APP_PREFIX, dependencies=[
        Depends(Authorization())
    ]
)
