from datetime import date

from sqlalchemy import Date, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from app.shared_resources.models import BaseModel


class PublicationModel(BaseModel):
    __tablename__ = "publications"

    upload_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("uploads.id", ondelete="RESTRICT"), index=True, nullable=False
    )

    xml_file_name: Mapped[str] = mapped_column(
        String(255), nullable=False
    )

    article_id: Mapped[str | None] = mapped_column(
        String(100), nullable=True
    )

    id_materia: Mapped[str | None] = mapped_column(
        String(100), nullable=True
    )

    title: Mapped[str | None] = mapped_column(
        String(500), nullable=True
    )

    ementa: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )

    text: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )

    pub_date: Mapped[date | None] = mapped_column(
        Date, nullable=True
    )

    __table_args__ = (
        UniqueConstraint(
            "upload_id", "xml_file_name", name="uq_publications_upload_xml"
        ),
    )
