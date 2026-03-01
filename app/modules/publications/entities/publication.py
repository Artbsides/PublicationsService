from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

from app.modules.publications.entities.source_file import SourceFileEntity


class PublicationEntity(BaseModel):
    id: UUID
    source_file: SourceFileEntity
    created_at: datetime
    updated_at: datetime | None = None
