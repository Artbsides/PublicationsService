from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel as PydanticBaseModel

from app.confs.database.session import get_current_session
from app.models import BaseModel


class BaseRepository:
    @property
    def session(self) -> AsyncSession:
        return get_current_session()

    def to_entity(
        self, entity: PydanticBaseModel, data: BaseModel
    ) -> PydanticBaseModel:
        return entity.model_validate(data, from_attributes=True)
