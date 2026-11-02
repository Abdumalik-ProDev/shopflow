"""Customer database model."""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import Uuid

from app.core.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    customer_unique_id: Mapped[str] = mapped_column(
        String(100), unique=True, index=True, nullable=False
    )
    customer_zip_code_prefix: Mapped[str] = mapped_column(String(20), default="", nullable=False)
    customer_city: Mapped[str] = mapped_column(String(100), default="", nullable=False)
    customer_state: Mapped[str] = mapped_column(String(10), default="", nullable=False)
    user_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
