from uuid import UUID
from datetime import datetime
from pydantic import Field, BaseModel

from app.modules.uploads.schemas.enums import UploadStatusEnum


class UploadResponse:
    class Create(BaseModel):
        id: UUID = Field(
            title="ID",
            description="Unique identifier",
        )

        filename: str = Field(
            title="Filename",
            description="Uploaded filename",
        )

        status: UploadStatusEnum = Field(
            title="Status",
            description="Upload current processing status",
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

    class ReadOne(Create):
        ...
