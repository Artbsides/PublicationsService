import boto3

from uuid import uuid4
from fastapi import Depends
from botocore.client import Config

from app.confs.environment import settings
from app.modules.publications.v1.dtos.publication import PublicationDto
from app.modules.publications.v1.repository import PublicationRepository


class PublicationService:
    def __init__(self, publication_repository: PublicationRepository = Depends()) -> None:
        self.publication_repository = publication_repository

    async def create(self, data: PublicationDto.Create) -> None:
        return await self.publication_repository.create()

    async def read(self) -> None:
        return await self.publication_repository.read()

    async def read_one(self) -> None:
        return await self.publication_repository.read_one()
