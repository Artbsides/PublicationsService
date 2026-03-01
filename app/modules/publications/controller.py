from fastapi import Depends, Form, status

from app.modules.publications.dtos.article import ArticleDto
from app.modules.publications.dtos.publication import PublicationDto
from app.modules.publications.responses.articles import ArticleResponse
from app.modules.publications.responses.publication import PublicationResponse
from app.modules.publications.service import PublicationService
from app.routers.router import router


router_settings = {
    "tags": ["Publications"],
}


@router.post("/publications",
    **router_settings, status_code=status.HTTP_202_ACCEPTED
)
async def create(
    data: PublicationDto.Create = Form(), publication_service: PublicationService = Depends()
) -> PublicationResponse.Create:
    return await publication_service.create(data)


@router.get("/publications", **router_settings)
async def retrieve_pubications(
    publication_service: PublicationService = Depends()
) -> list[PublicationResponse.Read]:
    return await publication_service.retrieve_pubications()


@router.get("/publications/{id}", **router_settings)
async def retrieve_pubication(
    parameters: PublicationDto.ReadOne = Depends(), publication_service: PublicationService = Depends()
) -> PublicationResponse.ReadOne:
    return await publication_service.retrieve_pubication(parameters)


@router.get("/publications/{publication_id}/articles", **router_settings)
async def retrieve_articles(
    parameters: ArticleDto.Read = Depends(), publication_service: PublicationService = Depends()
) -> list[ArticleResponse.Read]:
    return await publication_service.retrieve_articles(parameters)
