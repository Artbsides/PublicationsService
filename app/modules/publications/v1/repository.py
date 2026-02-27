from app.shared_resources.repositories import BaseRepository


class PublicationRepository(BaseRepository):
    async def create(self) -> None:
        query = ()
        query_result = await self.session.execute(query)

        return query_result

    async def create_outbox(self) -> None:
        query = ()
        query_result = await self.session.execute(query)

        return query_result

    async def read(self) -> None:
        return None

    async def read_one(self) -> None:
        return None
