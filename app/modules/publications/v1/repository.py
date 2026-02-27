from uuid import UUID

from sqlalchemy import insert

from app.modules.publications.v1.entities.upload import UploadEntity
from app.modules.publications.v1.models.uploads import UploadModel
from app.shared_resources.models import OutboxEvent
from app.shared_resources.repositories import BaseRepository


class PublicationRepository(BaseRepository):
    async def create_upload(
        self, *, original_filename: str, storage_key: str, content_type: str, size_bytes: int
    ) -> UploadEntity:
        query = (
            insert(UploadModel).values(
                original_filename=original_filename,
                storage_key=storage_key,
                content_type=content_type,
                size_bytes=size_bytes,
            )
            .returning(UploadModel)
        )

        query_result = await self.session.execute(query)

        return UploadEntity(
            **query_result.scalar_one().__dict__
        )

    async def create_outbox(
        self, *, aggregate_id: UUID, event_type: str, payload: dict, aggregate_type: str = "upload"
    ) -> None:
        query = (
            insert(OutboxEvent).values(
                aggregate_type=aggregate_type,
                aggregate_id=aggregate_id,
                event_type=event_type,
                payload=payload,
            )
            .returning(OutboxEvent)
        )

        await self.session.execute(query)

    async def create_publications(self) -> None:
        query = ()
        query_result = await self.session.execute(query)

        return query_result

    async def read(self) -> None:
        return None

    async def read_one(self) -> None:
        return None
