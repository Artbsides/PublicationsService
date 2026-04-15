from dishka import Provider, Scope, provide_all

from app.modules.publications.repository import PublicationRepository
from app.modules.publications.service import PublicationService


class PublicationProvider(Provider):
    wiring = provide_all(
        PublicationService, scope=Scope.REQUEST, recursive=True,
    )
