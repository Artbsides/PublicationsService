from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

from app.modules.uploads.schemas.enums import UploadStatusEnum


class UploadEntity(BaseModel):
    id: UUID
    filename: str
    storage_key: str
    status: UploadStatusEnum
    created_at: datetime
    updated_at: datetime | None = None
