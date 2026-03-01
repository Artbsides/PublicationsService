from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field

from app.enums import SourceFileStatusEnum
from app.modules.publications.responses.source_file import SourceFileResponse


class PublicationResponse:
    class Create(BaseModel):
        id: UUID = Field(
            title="ID",
            description="Unique identifier",
        )

        status: SourceFileStatusEnum = Field(
            title="Status",
            description="Current status of source file processing",
        )

        created_at: datetime = Field(
            title="Created At",
            description="Creation date and time",
        )

        updated_at: datetime | None = Field(
            title="Updated At",
            description="Last update date and time",
            default=None,
        )

    class Read(BaseModel):
        id: UUID = Field(
            title="ID",
            description="Unique identifier",
        )

        source_file: SourceFileResponse.Read = Field(
            title="Status",
            description="Current status of source file processing",
        )

        created_at: datetime = Field(
            title="Created At",
            description="Creation date and time",
        )

        updated_at: datetime | None = Field(
            title="Updated At",
            description="Last update date and time",
            default=None,
        )

    class ReadOne(Read):
        ...
