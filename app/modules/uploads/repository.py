from sqlalchemy import insert, select, update

from app.models import UploadModel
from app.core.database import BaseRepository
from app.modules.uploads.schemas.dtos import UploadDto
from app.modules.uploads.schemas.entities import UploadEntity


class UploadRepository(BaseRepository):
    async def create_upload(
        self, *, data: UploadDto.Create,
    ) -> UploadEntity:
        query = (
            insert(UploadModel).values(
                data.model_dump(exclude_unset=True)
            )
            .returning(UploadModel)
        )

        return self.to_entity(
            UploadEntity, (await self.session.execute(query)).scalar_one()
        )

    async def update_upload(
        self, *, filters: UploadDto.Read, data: UploadDto.Update
    ) -> UploadEntity | None:
        query = (
            update(UploadModel).where(
                *self.to_filters(UploadModel, filters)
            )
            .values(
                data.model_dump(exclude_unset=True)
            )
            .returning(UploadModel)
        )

        return self.to_entity(
            UploadEntity, (await self.session.execute(query)).scalar_one_or_none()
        )


    async def retrieve_uploads(self) -> list[UploadEntity]:
        query = select(UploadModel)

        return self.to_entities(
            UploadEntity, (await self.session.execute(query)).scalars().all()
        )

    async def retrieve_upload(
        self, *, filters: UploadDto.ReadOne
    ) -> UploadEntity:
        query = (
            select(UploadModel).where(
                *self.to_filters(UploadModel, filters)
            )
        )

        return self.to_entity(
            UploadEntity, (await self.session.execute(query)).scalar_one()
        )
