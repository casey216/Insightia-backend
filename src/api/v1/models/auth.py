import uuid
from datetime import datetime
from uuid_extensions import uuid7

from sqlalchemy import UUID, String, ForeignKey, DateTime, func, Boolean, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.api.v1.models.base import BaseModel


class RefreshToken(BaseModel):
    __tablename__ = "refresh_tokens"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID, primary_key=True, default=uuid7
    )
    token: Mapped[str] = mapped_column(
        String(150), unique=True, nullable=False, index=True
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID, ForeignKey("users.id"), index=True, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    revoked: Mapped[bool] = mapped_column(Boolean, default=False)

    user = relationship("User", back_populates="refresh_tokens")

    __table_args__ = (
        Index("ix_refresh_tokens_token_revoked", "token", "revoked"),
        Index("ix_refresh_tokens_user_id_revoked", "user_id", "revoked")
    )
