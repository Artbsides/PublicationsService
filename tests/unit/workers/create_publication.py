import pytest

from uuid import uuid4
from unittest.mock import AsyncMock, MagicMock, patch
from celery.exceptions import Retry

from workers.create_publication import create_publication


class TestWorker:
    @patch("workers.create_publication.run_async")
    @patch("workers.create_publication.PublicationService.create_publication")
    def create_publication_success_test(
        self,
        mock_create_publication: MagicMock,
        mock_run_async: MagicMock,
    ) -> None:
        upload_id = uuid4()

        create_publication(upload_id)

        mock_run_async.assert_called_once()
        mock_create_publication.assert_called_once()

        (
            _,
            kwargs
        ) = mock_create_publication.call_args

        assert kwargs["data"].upload_id == upload_id
        assert kwargs["is_last_retry"] is False

    @patch("workers.create_publication.run_async")
    @patch("workers.create_publication.create_publication.retry")
    def create_publication_failure_test(
        self,
        mock_retry: MagicMock,
        mock_run_async: MagicMock,
    ) -> None:
        mock_retry.side_effect = Retry()
        mock_run_async.side_effect = Exception()

        upload_id = uuid4()

        with pytest.raises(Retry):
            create_publication(upload_id)

        mock_retry.assert_called_once()
