from datetime import UTC, datetime
from sqlalchemy import Enum, String, DateTime, ForeignKey, text
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column
from sqlalchemy.dialects.postgresql import UUID, JSONB

from app.modules.uploads.schemas.enums import UploadStatusEnum


class BaseModel(DeclarativeBase):
    __abstract__ = True

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, nullable=False, server_default=text("gen_random_uuid()")
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=text("TIMEZONE('utc', CURRENT_TIMESTAMP)")
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, onupdate=lambda: datetime.now(datetime.now(UTC))
    )


class UploadModel(BaseModel):
    __tablename__ = "uploads"

    filename: Mapped[str] = mapped_column(
        String(255), nullable=False
    )

    storage_key: Mapped[str] = mapped_column(
        String(512), nullable=False, unique=True
    )

    status: Mapped[UploadStatusEnum] = mapped_column(
        Enum(UploadStatusEnum, name="upload_status"), nullable=False, index=True, server_default=text(
            f"'{UploadStatusEnum.PENDING.value}'"
        )
    )


class PublicationModel(BaseModel):
    __tablename__ = "publications"

    upload_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("uploads.id", ondelete="RESTRICT"), index=True, unique=True, nullable=False
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
