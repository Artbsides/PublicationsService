from fastapi import Depends, APIRouter
from dishka.integrations.fastapi import FromDishka, DishkaRoute

from app.core.authorization import Authorization
from app.modules.publications.service import PublicationService
from app.modules.publications.schemas.dtos import ArticleDto, PublicationDto
from app.modules.publications.schemas.responses import ArticleResponse, PublicationResponse


router = APIRouter(
    tags=["Publications"], route_class=DishkaRoute, dependencies=[
        Depends(Authorization())
    ]
)


@router.get("/publications")
async def retrieve_publications(
    publication_service: FromDishka[PublicationService]
) -> list[PublicationResponse.Read]:
    return await publication_service.retrieve_publications()


@router.get("/publications/{publication_id}")
async def retrieve_publication(
    publication_service: FromDishka[PublicationService], parameters: PublicationDto.ReadOne = Depends()
) -> PublicationResponse.ReadOne:
    return await publication_service.retrieve_publication(parameters)


@router.get("/publications/{publication_id}/articles")
async def retrieve_articles(
    publication_service: FromDishka[PublicationService], parameters: ArticleDto.Read = Depends()
) -> list[ArticleResponse.Read]:
    return await publication_service.retrieve_articles(parameters)


@router.get("/publications/{publication_id}/articles/{article_id}")
async def retrieve_article(
    publication_service: FromDishka[PublicationService], parameters: ArticleDto.ReadOne = Depends()
) -> ArticleResponse.ReadOne:
    return await publication_service.retrieve_article(parameters)
