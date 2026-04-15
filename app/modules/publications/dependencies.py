from dishka import Scope, Provider, provide_all

from app.modules.publications.service import PublicationService


class PublicationProvider(Provider):
    wiring = provide_all(
        PublicationService, scope=Scope.REQUEST, recursive=True,
    )
