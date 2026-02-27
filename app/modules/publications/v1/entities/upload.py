from uuid import UUID

from pydantic import BaseModel

from app.modules.publications.v1.enums.upload import UploadStatusEnum


class UploadEntity(BaseModel):
    id: UUID
    status: UploadStatusEnum
    storage_key: str
