from fastapi import Depends, Form, status

from app.modules.publications.v1.dtos.publication import PublicationDto
from app.routers.router import router
from app.modules.publications.v1.service import PublicationService


router_settings = {
    "tags": ["Publications"], "response_model_by_alias": False
}


@router.post("/publications/v1/uploads",
    **router_settings, status_code=status.HTTP_202_ACCEPTED
)
async def create(
    data: PublicationDto.Create = Form(), publication_service: PublicationService = Depends()
) -> None:
    return await publication_service.create(data)


@router.get("/publications/v1/uploads", **router_settings)
async def read(publication_service: PublicationService = Depends()) -> None:
    return await publication_service.read_one()


@router.get("/publications/v1/uploads/:upload_id", **router_settings)
async def read_one(publication_service: PublicationService = Depends()) -> None:
    return await publication_service.read_one()
