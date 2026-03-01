from uuid import UUID

from pydantic import BaseModel


class ArticleEntity(BaseModel):
    id: UUID
    publication_id: UUID
    data: dict
