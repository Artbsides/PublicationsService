import pytest

from uuid import uuid4
from faker import Faker
from unittest import mock

from app.modules.publications.controller import retrieve_article, retrieve_articles, retrieve_publication, retrieve_publications
from app.modules.publications.schemas.dtos import ArticleDto, PublicationDto
from app.modules.publications.schemas.entities import ArticleEntity, PublicationEntity


faker = Faker()


class TestPublicationController:
    @pytest.mark.asyncio
    async def retrieve_publications_success_test(self):
        mock_response = [
            PublicationEntity(
                id=uuid4(),
                upload_id=uuid4(),
                created_at=faker.date_time_this_year().isoformat(),
                updated_at=faker.date_time_this_year().isoformat(),
            )
        ]

        mock_service = mock.AsyncMock()
        mock_service.retrieve_publications.return_value = mock_response

        assert (
            await retrieve_publications(
                publication_service=mock_service
            )
        ) == mock_response

    @pytest.mark.asyncio
    async def retrieve_publication_success_test(self):
        mock_response = PublicationEntity(
            id=uuid4(),
            upload_id=uuid4(),
            created_at=faker.date_time_this_year().isoformat(),
            updated_at=faker.date_time_this_year().isoformat(),
        )

        mock_service = mock.AsyncMock()
        mock_service.retrieve_publication.return_value = mock_response

        assert (
            await retrieve_publication(
                parameters=PublicationDto.ReadOne(
                    id=mock_response.id
                ),
                publication_service=mock_service
            )
        ) == mock_response

    @pytest.mark.asyncio
    async def retrieve_articles_success_test(self):
        mock_response = [
            ArticleEntity(
                id=uuid4(),
                publication_id=uuid4(),
                data={
                    "id": uuid4(),
                    "name": faker.name(),
                },
                created_at=faker.date_time_this_year().isoformat(),
                updated_at=faker.date_time_this_year().isoformat(),
            )
        ]

        mock_service = mock.AsyncMock()
        mock_service.retrieve_articles.return_value = mock_response

        assert (
            await retrieve_articles(
                publication_service=mock_service
            )
        ) == mock_response

    @pytest.mark.asyncio
    async def retrieve_article_success_test(self):
        mock_response = ArticleEntity(
            id=uuid4(),
            publication_id=uuid4(),
            data={
                "id": uuid4(),
                "name": faker.name(),
            },
            created_at=faker.date_time_this_year().isoformat(),
            updated_at=faker.date_time_this_year().isoformat(),
        )

        mock_service = mock.AsyncMock()
        mock_service.retrieve_article.return_value = mock_response

        assert (
            await retrieve_article(
                parameters=ArticleDto.ReadOne(
                    id=mock_response.id, publication_id=mock_response.publication_id
                ),
                publication_service=mock_service
            )
        ) == mock_response
