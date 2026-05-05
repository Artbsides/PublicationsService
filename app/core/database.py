from pydantic import BaseModel as PydanticBaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import BaseModel


class BaseRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    def to_filters(
        self, model: BaseModel, data: PydanticBaseModel
    ) -> list:
        return [
            getattr(model, attribute) == value for attribute, value in data.model_dump(
                exclude_unset=True
            ).items()
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
