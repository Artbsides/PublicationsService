from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel as PydanticBaseModel

from app.confs.database.session import get_current_session
from app.models import BaseModel


class BaseRepository:
    @property
    def session(self) -> AsyncSession:
        return get_current_session()

    def to_filters(
        self, model: BaseModel, kwargs: dict
    ) -> list:
        return [
            getattr(model, attribute) == value for attribute, value in kwargs.items()
        ]

    def to_entity(
        self, entity: PydanticBaseModel, data: BaseModel | None
    ) -> PydanticBaseModel:
        return data and entity.model_validate(data, from_attributes=True)

    def to_entities(
        self, entity: PydanticBaseModel, data: list[BaseModel]
    ) -> list[PydanticBaseModel]:
        entities = []

        if isinstance(data, list):
            for item in data:
                entities.append(self.to_entity(entity, item))

        return entities
