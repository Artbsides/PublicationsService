from uuid import UUID

from fastapi import UploadFile
from pydantic import BaseModel, Field, field_validator


class PublicationDto:
    class Create(BaseModel):
        file: UploadFile

        @field_validator("file", mode="after")
        @classmethod
        def validate_file(cls, file: UploadFile) -> UploadFile:
            if not (file.filename or "").strip():
                raise ValueError("file name is required")

            if file.content_type not in ["application/zip", "application/x-zip-compressed"]:
                raise ValueError("file must be .zip")

            return file

    class ReadOne(BaseModel):
        id: UUID
