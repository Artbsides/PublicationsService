from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


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
            alias="metadata",
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

        model_config = ConfigDict(populate_by_name=True)

    class ReadOne(Read):
        ...
