import asyncio
from uuid import UUID

from app.confs.workers import get_application
from app.modules.publications.repository import PublicationRepository
from app.modules.publications.service import PublicationService


app = get_application()


@app.task(
    bind=True,
    max_retries=10,
    default_retry_delay=2,
    name="process_uploaded_file",
)
def process_uploaded_file(self, source_file_id: UUID):
    publication_service = PublicationService(
        PublicationRepository()
    )

    try:
        return asyncio.run(
            publication_service.process_source_file(
                source_file_id=source_file_id, is_last_retry=self.request.retries >= self.max_retries
            )
        )
    except Exception as exception:
        raise self.retry(exc=exception)


## TODO: celery types (.retry, .max_retries ...) - move broker and bucket methods to repository - create env vars to ensure_bindings at startup