"""Reviews infrastructure ORM models."""

import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, func, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from shopflow.shared.infrastructure.database.metadata import metadata


class Base(DeclarativeBase):
    metadata = metadata


class ReviewRow(Base):
    __tablename__ = "reviews"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("orders.id"), nullable=False)
    review_score: Mapped[int] = mapped_column(Integer, nullable=False)
    comment_title: Mapped[str | None] = mapped_column(Text, nullable=True)
    comment_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    order = relationship("OrderRow", lazy="selectin")


__all__ = ["Base", "ReviewRow"]
