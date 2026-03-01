from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

from app.enums import SourceFileStatusEnum


class SourceFileEntity(BaseModel):
    id: UUID
    filename: str
    storage_key: str
    status: SourceFileStatusEnum
    created_at: datetime
    updated_at: datetime | None = None
