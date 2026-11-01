"""Payments infrastructure ORM models."""

import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, func, Float, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from shopflow.shared.infrastructure.database.metadata import metadata


class Base(DeclarativeBase):
    metadata = metadata


class PaymentRow(Base):
    __tablename__ = "payments"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("orders.id"), nullable=False)
    payment_sequential: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    payment_type: Mapped[str] = mapped_column(String(50), nullable=False)
    payment_installments: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    payment_value: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    order = relationship("OrderRow", lazy="selectin")


__all__ = ["Base", "PaymentRow"]
