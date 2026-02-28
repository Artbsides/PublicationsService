from fastapi import Depends, Form, status

from app.modules.publications.dtos.publication import PublicationDto
from app.modules.publications.responses.publication import PublicationResponse
from app.modules.publications.service import PublicationService
from app.routers.router import router


router_settings = {
    "tags": ["Publications"], "response_model_by_alias": False
}


@router.post("/publications",
    **router_settings, status_code=status.HTTP_202_ACCEPTED
)
async def create(
    data: PublicationDto.Create = Form(), publication_service: PublicationService = Depends()
) -> PublicationResponse.Create:
    return await publication_service.create(data)
