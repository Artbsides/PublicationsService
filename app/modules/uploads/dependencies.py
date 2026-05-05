from dishka import Scope, Provider, provide_all

from app.modules.uploads.service import UploadService
from app.modules.uploads.repository import UploadRepository


class UploadProvider(Provider):
    service = provide_all(
        UploadService, UploadRepository, scope=Scope.REQUEST,
    )
