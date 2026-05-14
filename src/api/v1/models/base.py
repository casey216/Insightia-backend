import uuid
from datetime import date, datetime
from typing import Any

from sqlalchemy import inspect
from sqlalchemy.orm import Mapper

from src.api.db.database import Base


class ModelMixin:
    @staticmethod
    def _mapper(obj: object) -> Mapper:
        """Returns the mapper for a model instance"""
        return inspect(obj, raiseerr=True).mapper
    

    @staticmethod
    def _serialize(value: Any) -> Any:
        """Coerce non-JSON-native types to serializable equivalents."""
        if isinstance(value, uuid.UUID):
            return str(value)
        if isinstance(value, datetime):
            return value.strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            )
        return value
        

    def __repr__(self) -> str:
        mapper = self._mapper(self)
        pk_names = [
            col.key for col in mapper.primary_key if col.key is not None
        ]
        pk_pairs = ", ".join(
            f"{name}={getattr(self, name)!r}" for name in pk_names
        )
        return f"<{self.__class__.__name__} ({pk_pairs})"
    

    def to_dict(self, exclude: set[str] | None = None) -> dict[str, Any]:
        exclude = exclude or set()
        mapper = self._mapper(self)
        return {
            col.key: self._serialize(getattr(self, col.key))
            for col in mapper.column_attrs
            if col.key is not None and col.key not in exclude
        }


class BaseModel(Base, ModelMixin):
    __abstract__ = True
