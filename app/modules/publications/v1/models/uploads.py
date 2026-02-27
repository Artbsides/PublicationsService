from sqlalchemy import Enum, Integer, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column

from app.modules.publications.v1.enums.upload import UploadEnum
from app.shared_resources.models import BaseModel


class UploadModel(BaseModel):
    __tablename__ = "uploads"

    original_filename: Mapped[str] = mapped_column(
        String(255), nullable=False
    )

    storage_key: Mapped[str] = mapped_column(
        String(512), nullable=False, unique=True
    )

    content_type: Mapped[str] = mapped_column(
        String(100), nullable=False
    )

    size_bytes: Mapped[int] = mapped_column(
        Integer, nullable=False
    )

    status: Mapped[UploadEnum] = mapped_column(
        Enum(UploadEnum, name="upload_status"), nullable=False, index=True, server_default=text(
            f"'{UploadEnum.PENDING.value}'"
        )
    )

    error_message: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )
