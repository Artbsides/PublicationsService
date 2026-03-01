from uuid import UUID

from pydantic import BaseModel


class ArticleDto:
    class Read(BaseModel):
        publication_id: UUID
