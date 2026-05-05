from dishka import Scope, Provider, provide_all

from app.modules.publications.service import PublicationService
from app.modules.publications.repository import PublicationRepository


class PublicationProvider(Provider):
    service = provide_all(
        PublicationService, PublicationRepository, scope=Scope.REQUEST,
    )
