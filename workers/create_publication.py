from __future__ import annotations

from uuid import UUID
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from celery import Task

from app.core.config.worker import run_async, get_application
from app.modules.uploads.service import UploadService
from app.modules.uploads.repository import UploadRepository
from app.modules.publications.service import PublicationService
from app.modules.publications.repository import PublicationRepository
from app.modules.publications.schemas.dtos import PublicationDto


app = get_application()


@app.task(
    bind=True,
    max_retries=5,
    default_retry_delay=2,
    name="create_publication",
)
def create_publication(self: Task, upload_id: UUID) -> None:
    publication_service = PublicationService(
        upload_service=UploadService(
            upload_repository=UploadRepository()
        ),
        publication_repository=PublicationRepository()
    )

    try:
        run_async(
            publication_service.create_publication(
                data=PublicationDto.Create(upload_id=upload_id), is_last_retry=(
                    self.request.retries >= self.max_retries
                )
            )
        )
    except Exception as exception:
        raise self.retry(exc=exception) from exception
