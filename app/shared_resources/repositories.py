from sqlalchemy.ext.asyncio import AsyncSession
from app.confs.database.session import get_current_session


class BaseRepository:
    @property
    def session(self) -> AsyncSession:
        return get_current_session()
