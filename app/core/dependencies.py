from dishka import make_container, make_async_container
from dishka.integrations.fastapi import FastapiProvider

from app.modules.uploads.dependencies import UploadProvider
from app.modules.publications.dependencies import PublicationProvider


providers = (
    PublicationProvider(),
    UploadProvider(),
)


def build_container():
    return make_async_container(
        FastapiProvider(), *providers
    )


def build_worker_container():
    return make_container(*providers)
