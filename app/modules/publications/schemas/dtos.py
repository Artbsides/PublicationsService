from uuid import UUID
from pydantic import Field, BaseModel, ConfigDict


class PublicationDto:
    class Create(BaseModel):
        upload_id: UUID

    class Read(BaseModel):
        upload_id: UUID

    class ReadOne(BaseModel):
        model_config = ConfigDict(populate_by_name=True)

        id: UUID = Field(
            alias="publication_id"
        )


class ArticleDto:
    class Create(BaseModel):
        publication_id: UUID
        idempotency_key: UUID
        data: dict

    class Read(BaseModel):
        publication_id: UUID

    class ReadOne(BaseModel):
        model_config = ConfigDict(populate_by_name=True)

        publication_id: UUID

        id: UUID = Field(
            alias="article_id"
        )
