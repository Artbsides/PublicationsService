from fastapi import Depends, APIRouter

from app.core.authorization import Authorization
from app.modules.publications.service import PublicationService
from app.modules.publications.schemas.dtos import ArticleDto, PublicationDto
from app.modules.publications.schemas.responses import ArticleResponse, PublicationResponse


router = APIRouter(
    tags=["Publications"], dependencies=[
        Depends(Authorization())
    ]
)


@router.get("/publications")
async def retrieve_publications(
    publication_service: PublicationService = Depends()
) -> list[PublicationResponse.Read]:
    return await publication_service.retrieve_publications()


@router.get("/publications/{publication_id}")
async def retrieve_publication(
    parameters: PublicationDto.ReadOne = Depends(), publication_service: PublicationService = Depends()
) -> PublicationResponse.ReadOne:
    return await publication_service.retrieve_publication(parameters)


@router.get("/publications/{publication_id}/articles")
async def retrieve_articles(
    parameters: ArticleDto.Read = Depends(), publication_service: PublicationService = Depends()
) -> list[ArticleResponse.Read]:
    return await publication_service.retrieve_articles(parameters)


@router.get("/publications/{publication_id}/articles/{article_id}")
async def retrieve_article(
    parameters: ArticleDto.ReadOne = Depends(), publication_service: PublicationService = Depends()
) -> ArticleResponse.ReadOne:
    return await publication_service.retrieve_article(parameters)
