from dishka import Scope, Provider, provide_all

from app.modules.uploads.service import UploadService


class UploadProvider(Provider):
    wiring = provide_all(
        UploadService, scope=Scope.REQUEST, recursive=True,
    )
