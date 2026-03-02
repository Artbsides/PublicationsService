from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class PublicationEntity(BaseModel):
    id: UUID
    upload_id: UUID
    created_at: datetime
    updated_at: datetime | None = None


class ArticleEntity(BaseModel):
    id: UUID
    publication_id: UUID
    data: dict
    created_at: datetime
    updated_at: datetime | None = None
