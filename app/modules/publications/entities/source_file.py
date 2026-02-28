from uuid import UUID
from pydantic import BaseModel

from app.enums import SourceFileStatusEnum


class SourceFileEntity(BaseModel):
    id: UUID
    status: SourceFileStatusEnum
