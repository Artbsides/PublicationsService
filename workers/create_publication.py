from uuid import UUID
from celery import Task, shared_task

from app.core.dependencies import build_worker_container
from app.core.config.worker import run_async
from app.modules.publications.service import PublicationService
from app.modules.publications.schemas.dtos import PublicationDto


@shared_task(
    bind=True,
    max_retries=5,
    default_retry_delay=2,
    name="create_publication",
)
def create_publication(
    self: Task, upload_id: UUID
) -> None:
    async def execute_task() -> None:
        async with build_worker_container() as container:
            publication_service = await container.get(PublicationService)

            await publication_service.create_publication(
                data=PublicationDto.Create(upload_id=upload_id), is_last_retry=(
                    self.request.retries >= self.max_retries
                ),
            )

    try:
        run_async(
            execute_task()
        )
    except Exception as exception:
        raise self.retry(exc=exception) from exception
