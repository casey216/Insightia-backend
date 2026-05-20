import uuid
from datetime import datetime

from sqlalchemy import Boolean, String, DateTime, UUID, func
from sqlalchemy.orm import mapped_column, Mapped, relationship
from uuid_extensions import uuid7

from .base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid7)
    github_id: Mapped[str] = mapped_column(String(100), unique=True)
    username: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, index=True, unique=True)
    avatar_url: Mapped[str] = mapped_column(String(500))
    role: Mapped[str] = mapped_column(String(100), default="analyst")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    last_login_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
        )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    refresh_tokens = relationship("RefreshToken", back_populates="user")
