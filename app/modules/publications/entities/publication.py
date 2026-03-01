from uuid import UUID

from pydantic import BaseModel


class PublicationEntity(BaseModel):
    id: UUID
    source_file_id: UUID
