from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class ArticleEntity(BaseModel):
    id: UUID
    publication_id: UUID
    data: dict
    created_at: datetime
    updated_at: datetime | None = None
