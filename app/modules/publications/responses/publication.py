from uuid import UUID
from pydantic import BaseModel, Field

from app.enums import SourceFileStatusEnum


class PublicationResponse:
    class Create(BaseModel):
        id: UUID = Field(
            title="ID",
            description="Unique identifier for the publication upload"
        )

        status: SourceFileStatusEnum = Field(
            title="Status",
            description="Current status of the publication upload"
        )
