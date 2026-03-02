import pytest

from uuid import uuid4
from unittest import mock
from celery.exceptions import Retry

from workers.create_publication import create_publication


class TestWorker:
    @mock.patch("workers.create_publication.run_async")
    @mock.patch("workers.create_publication.PublicationService")
    @mock.patch("workers.create_publication.UploadService")
    @mock.patch("workers.create_publication.PublicationRepository")
    def create_publication_success_test(
        self,
        mock_publication_repository,
        mock_upload_service,
        mock_publication_service,
        mock_run_async
    ):
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

    @mock.patch("workers.create_publication.run_async")
    @mock.patch("workers.create_publication.PublicationService")
    @mock.patch("workers.create_publication.UploadService")
    @mock.patch("workers.create_publication.PublicationRepository")
    @mock.patch("workers.create_publication.create_publication.retry")
    def create_publication_failure_test(
        self,
        mock_retry,
        mock_publication_repository,
        mock_upload_service,
        mock_publication_service,
        mock_run_async,
    ):
        mock_retry.side_effect = Retry()
        mock_run_async.side_effect = Exception()

        upload_id = uuid4()

        with pytest.raises(Retry):
            create_publication(upload_id)

        mock_retry.assert_called_once()
