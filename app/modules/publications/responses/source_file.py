from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.enums import SourceFileStatusEnum


class SourceFileResponse:
    class Create(BaseModel):
        id: UUID = Field(
            title="ID",
            description="Unique identifier",
        )

        filename: str = Field(
            title="Filename",
            description="Uploaded",
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

    class Read(Create):
        ...