from fastapi import Form, Depends, status

from app.routers.router import router
from app.modules.uploads.service import UploadService
from app.modules.uploads.schemas.dtos import UploadDto
from app.modules.uploads.schemas.responses import UploadResponse


router_settings = {
    "tags": ["Uploads"],
}


@router.post("/uploads",
    **router_settings, status_code=status.HTTP_202_ACCEPTED
)
async def create_upload(
    data: UploadDto.Upload = Form(), upload_service: UploadService = Depends()
) -> UploadResponse.Create:
    return await upload_service.create_upload(data)


@router.get("/uploads",**router_settings,)
async def retrieve_uploads(upload_service: UploadService = Depends()) -> list[UploadResponse.Read]:
    return await upload_service.retrieve_uploads()


@router.get("/uploads/{upload_id}",**router_settings)
async def retrieve_upload(
    parameters: UploadDto.ReadOne = Depends(), upload_service: UploadService = Depends()
) -> UploadResponse.ReadOne:
    return await upload_service.retrieve_upload(parameters)
