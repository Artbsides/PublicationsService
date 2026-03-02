from uuid import UUID
from datetime import datetime
from pydantic import Field, BaseModel


class PublicationResponse:
    class Read(BaseModel):
        id: UUID = Field(
            title="ID",
            description="Unique identifier",
        )

        upload_id: UUID = Field(
            title="Upload ID",
            description="Unique identifier of the related upload",
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


class ArticleResponse:
    class Read(BaseModel):
        id: UUID = Field(
            title="ID",
            description="Unique identifier",
        )

        publication_id: UUID = Field(
            title="Publication ID",
            description="Unique identifier of the publication",
        )

        data: dict = Field(
            title="Data",
            description="Extracted metadata",
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
