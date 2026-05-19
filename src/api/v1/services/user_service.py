from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..models.user import User
from src.api.core.exceptions import ResourceNotFoundError, InvalidIdError


class UserService:
    """Handles all business logic for user account management."""

    @staticmethod
    def create(user_data: dict, db: Session) -> User | None:
        db_user = User(**user_data)
        db.add(db_user)

        try:
            db.commit()
            db.refresh(db_user)
            return db_user
        except IntegrityError:
            db.rollback()
            github_id = user_data.get("github_id", "")
            db_user = UserService.get_user_by_github_id(
                github_id, db
            )
            if db_user:
                return UserService.update(
                    str(db_user.id),
                    user_data,
                    db
                )
    
    @staticmethod
    def fetch_all(db: Session) -> list[User]:
        return db.query(User).all()
    
    @staticmethod
    def get_user_by_id(id: str, db: Session) -> User | None:
        try:
            db_user = db.get(User, UUID(id))
            if not db_user:
                raise ResourceNotFoundError("User")
            return db_user
        except ValueError:
            raise InvalidIdError("User")
        
    @staticmethod
    def get_user_by_github_id(id: str, db: Session) -> User | None:
        db_user = db.query(User).filter_by(github_id=id).first()
        return db_user
    
    @staticmethod
    def get_user_by_email(email: str, db: Session) -> User | None:
        db_user = db.query(User).filter_by(email=email).first()
        return db_user
    
    @staticmethod
    def update(id: str, user_data: dict, db: Session) -> User | None:
        try:
            db_user = UserService.get_user_by_id(id, db)
            
            changed = False
            user_data["updated_at"] = datetime.now(timezone.utc)
            for key, value in user_data.items():
                if value is None:
                    continue

                if hasattr(db_user, key) and getattr(db_user, key) != value:
                    setattr(user_data, key, value)
                    changed = True

            if changed:
                db.commit()
                db.refresh(db_user)

            return db_user
        except ValueError:
            raise

    @staticmethod
    def delete(id: str, db: Session) -> None:
        db_user = db.get(User, UUID(id))
        if not db_user:
            raise
        db.delete(db_user)
        db.commit()
        return
