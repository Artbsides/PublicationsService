from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, Index, Integer, String, Text, text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.shared_resources.enums import OutboxEventStatusEnum


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


class OutboxEvent(BaseModel):
    __tablename__ = "outbox_events"

    aggregate_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False
    )

    aggregate_type: Mapped[str] = mapped_column(
        String(100), nullable=False
    )

    event_type: Mapped[str] = mapped_column(
        String(150), nullable=False
    )

    payload: Mapped[dict] = mapped_column(
        JSONB, nullable=False
    )

    status: Mapped[OutboxEventStatusEnum] = mapped_column(
        Enum(OutboxEventStatusEnum, name="outbox_event_status"), nullable=False, index=True, server_default=text(
            f"'{OutboxEventStatusEnum.PENDING.value}'"
        )
    )

    retry_count: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default=text("0")
    )

    error_message: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )

    published_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    __table_args__ = (
        Index(
            "ix_outbox_status_created_at", "status", "created_at"
        ),
    )
