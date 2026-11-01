"""Sellers infrastructure persistence models."""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import String, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from shopflow.shared.infrastructure.database.metadata import metadata


class Base(DeclarativeBase):
    metadata = metadata


class SellerRow(Base):
    __tablename__ = "sellers"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    seller_zip_code_prefix: Mapped[str] = mapped_column(String(20), nullable=False)
    seller_city: Mapped[str] = mapped_column(String(100), nullable=False)
    seller_state: Mapped[str] = mapped_column(String(10), nullable=False)
    user_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


__all__ = ["Base", "SellerRow"]
