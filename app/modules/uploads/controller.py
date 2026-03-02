from typing import Annotated
from fastapi import Form, Depends, APIRouter, status

from app.core.authorization import Authorization
from app.modules.uploads.service import UploadService
from app.modules.uploads.schemas.dtos import UploadDto
from app.modules.uploads.schemas.responses import UploadResponse


router = APIRouter(
    tags=["Uploads"], dependencies=[
        Depends(Authorization())
    ]
)


@router.post("/uploads",
    status_code=status.HTTP_202_ACCEPTED
)
async def create_upload(
    data: Annotated[UploadDto.Upload, Form()], upload_service: UploadService = Depends()
) -> UploadResponse.Create:
    return await upload_service.create_upload(data)


@router.get("/uploads")
async def retrieve_uploads(upload_service: UploadService = Depends()) -> list[UploadResponse.Read]:
    return await upload_service.retrieve_uploads()


@router.get("/uploads/{upload_id}")
async def retrieve_upload(
    parameters: UploadDto.ReadOne = Depends(), upload_service: UploadService = Depends()
) -> UploadResponse.ReadOne:
    return await upload_service.retrieve_upload(parameters)
