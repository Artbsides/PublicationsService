from uuid import UUID
from celery import Task
from dishka.integrations.celery import DishkaTask, FromDishka

from app.core.config.worker import run_async, get_application
from app.modules.publications.service import PublicationService
from app.modules.publications.schemas.dtos import PublicationDto


app = get_application()


@app.task(
    bind=True,
    base=DishkaTask,
    max_retries=5,
    default_retry_delay=2,
    name="create_publication",
)
def create_publication(
    self: Task,
    upload_id: UUID,
    publication_service: FromDishka[PublicationService]
) -> None:
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
