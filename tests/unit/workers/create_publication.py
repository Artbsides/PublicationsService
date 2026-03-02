import pytest

from uuid import uuid4
from unittest.mock import MagicMock, patch
from celery.exceptions import Retry

from workers.create_publication import create_publication


class TestWorker:
    @patch("workers.create_publication.run_async")
    @patch("workers.create_publication.PublicationService")
    @patch("workers.create_publication.UploadService")
    @patch("workers.create_publication.PublicationRepository")
    def create_publication_success_test(
        self,
        mock_publication_repository: MagicMock,
        mock_upload_service: MagicMock,
        mock_publication_service: MagicMock,
        mock_run_async: MagicMock,
    ) -> None:
        upload_id = uuid4()

        create_publication(upload_id)

        mock_publication_service.return_value.create_publication.assert_called_once()

        (
            _,
            kwargs
        ) = mock_publication_service.return_value.create_publication.call_args

        assert kwargs["data"].upload_id == upload_id
        assert kwargs["is_last_retry"] is False

        mock_run_async.assert_called_once_with(
            mock_publication_service.return_value.create_publication.return_value
        )

    @patch("workers.create_publication.run_async")
    @patch("workers.create_publication.PublicationService")
    @patch("workers.create_publication.UploadService")
    @patch("workers.create_publication.PublicationRepository")
    @patch("workers.create_publication.create_publication.retry")
    def create_publication_failure_test(
        self,
        mock_retry: MagicMock,
        mock_publication_repository: MagicMock,
        mock_upload_service: MagicMock,
        mock_publication_service: MagicMock,
        mock_run_async: MagicMock,
    ) -> None:
        mock_retry.side_effect = Retry()
        mock_run_async.side_effect = Exception()

        upload_id = uuid4()

        with pytest.raises(Retry):
            create_publication(upload_id)

        mock_retry.assert_called_once()
