import io
import pytest
import secrets

from uuid import uuid4
from faker import Faker
from fastapi import UploadFile
from unittest import mock

from app.modules.uploads.controller import create_upload, retrieve_upload, retrieve_uploads
from app.modules.uploads.schemas.dtos import UploadDto
from app.modules.uploads.schemas.enums import UploadStatusEnum
from app.modules.uploads.schemas.entities import UploadEntity


faker = Faker()


class TestUploadController:
    @pytest.mark.asyncio
    async def create_upload_success_test(self) -> None:
        mock_response = UploadEntity(
            id=uuid4(),
            filename=faker.file_name(extension="zip"),
            storage_key=f"{faker.uuid4()}.zip",
            status=UploadStatusEnum.PENDING,
            created_at=faker.date_time_this_year().isoformat(),
            updated_at=faker.date_time_this_year().isoformat(),
        )

        mock_service = mock.AsyncMock()
        mock_service.create_upload.return_value = mock_response

        file = UploadFile(
            file=io.BytesIO(b"content"), filename="test.zip", headers={"content-type": "application/zip"}
        )

        assert (
            await create_upload(
                data=UploadDto.Upload(file=file), upload_service=mock_service
            )
        ) == mock_response

    @pytest.mark.asyncio
    async def retrieve_uploads_success_test(self) -> None:
        mock_response = [
            UploadEntity(
                id=uuid4(),
                filename=faker.file_name(extension="zip"),
                storage_key=f"{faker.uuid4()}.zip",
                status=secrets.choice(list(UploadStatusEnum)),
                created_at=faker.date_time_this_year().isoformat(),
                updated_at=faker.date_time_this_year().isoformat(),
            )
        ]

        mock_service = mock.AsyncMock()
        mock_service.retrieve_uploads.return_value = mock_response

        assert (
            await retrieve_uploads(
                upload_service=mock_service
            )
        ) == mock_response

    @pytest.mark.asyncio
    async def retrieve_upload_success_test(self) -> None:
        mock_response = UploadEntity(
            id=uuid4(),
            filename=faker.file_name(extension="zip"),
            storage_key=f"{faker.uuid4()}.zip",
            status=secrets.choice(list(UploadStatusEnum)),
            created_at=faker.date_time_this_year().isoformat(),
            updated_at=faker.date_time_this_year().isoformat(),
        )

        mock_service = mock.AsyncMock()
        mock_service.retrieve_upload.return_value = mock_response

        assert (
            await retrieve_upload(
                parameters=UploadDto.ReadOne(
                    id=mock_response.id
                ),
                upload_service=mock_service
            )
        ) == mock_response
