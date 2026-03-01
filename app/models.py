from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from app.enums import SourceFileStatusEnum


class BaseModel(DeclarativeBase):
    __abstract__ = True

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, nullable=False, server_default=text("gen_random_uuid()")
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=text("TIMEZONE('utc', CURRENT_TIMESTAMP)")
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, onupdate=lambda: datetime.now(timezone.utc)
    )


class SourceFileModel(BaseModel):
    __tablename__ = "source_files"

    filename: Mapped[str] = mapped_column(
        String(255), nullable=False
    )

    storage_key: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True
    )

    status: Mapped[SourceFileStatusEnum] = mapped_column(
        Enum(SourceFileStatusEnum, name="source_file_status"), nullable=False, index=True, server_default=text(
            f"'{SourceFileStatusEnum.PENDING.value}'"
        )
    )

    publication = relationship(
        "PublicationModel", back_populates="source_file"
    )


class PublicationModel(BaseModel):
    __tablename__ = "publications"

    source_file_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("source_files.id", ondelete="RESTRICT"), index=True, unique=True, nullable=False
    )

    source_file = relationship(
        "SourceFileModel", back_populates="publication"
    )


class ArticleModel(BaseModel):
    __tablename__ = "articles"

    idempotency_key: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), index=True, unique=True, nullable=False
    )

    publication_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("publications.id", ondelete="RESTRICT"), index=True, nullable=False
    )

    data: Mapped[dict] = mapped_column(
        JSONB, nullable=False
    )
