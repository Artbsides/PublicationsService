from dishka import Provider, Scope, provide_all

from app.modules.uploads.repository import UploadRepository
from app.modules.uploads.service import UploadService


class UploadProvider(Provider):
    wiring = provide_all(
        UploadService, scope=Scope.REQUEST, recursive=True,
    )
