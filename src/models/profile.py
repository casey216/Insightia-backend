from datetime import datetime
import uuid
from uuid_extensions import uuid7

from sqlalchemy import String, Integer, DateTime, UUID, Float, func
from sqlalchemy.orm import mapped_column, Mapped

from src.models.base import BaseModel

class Profile(BaseModel):
    __tablename__ = "profiles"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid7)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    gender: Mapped[str] = mapped_column(String(100), nullable=False)
    gender_probability: Mapped[float] = mapped_column(Float, nullable=False)
    sample_size: Mapped[int] = mapped_column(Integer, nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    age_group: Mapped[str] = mapped_column(String(100), nullable=False)
    country_id: Mapped[str] = mapped_column(String(2), nullable=False)
    country_probability: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
