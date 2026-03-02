from uuid import UUID
from fastapi import UploadFile
from pydantic import Field, BaseModel, ConfigDict, field_validator

from app.modules.uploads.schemas.enums import UploadStatusEnum


class UploadDto:
    class Upload(BaseModel):
        file: UploadFile

        @field_validator("file", mode="after")
        @classmethod
        def validate_file(cls, file: UploadFile) -> UploadFile:
            if not (file.filename or "").strip():
                raise ValueError("file name is required")

            if file.content_type not in ["application/zip", "application/x-zip-compressed"]:
                raise ValueError("file must be .zip")

            return file

    class Create(BaseModel):
        filename: str
        storage_key: str

    class Read(BaseModel):
        id: UUID
        status: UploadStatusEnum | None = None

    class ReadOne(BaseModel):
        model_config = ConfigDict(populate_by_name=True)

        id: UUID = Field(
            alias="upload_id"
        )

    class Update(BaseModel):
        status: UploadStatusEnum
