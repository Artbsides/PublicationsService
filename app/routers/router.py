from fastapi import Depends, APIRouter

from app.confs.environment import settings
from app.utils.authorization import Authorization


router = APIRouter(
    prefix=settings.APP_PREFIX, dependencies=[
        Depends(Authorization())
    ]
)
