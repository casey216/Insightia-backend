from sqlalchemy.orm import Session

from src.models.profile import Profile
from src.schemas.profile import ProfileCreate
from src.services.agify import fetch_agify_data
from src.services.genderize import fetch_genderize_data
from src.services.nationalize import fetch_nationalize_data
from src.utils.helpers import process_responses


class ProfileService:
    """Service layer business logic for profiles."""

    @staticmethod
    async def create_profile(name: str, db: Session) -> Profile:
        agify_data = await fetch_agify_data(name)
        genderize_data = await fetch_genderize_data(name)
        nationalize_data = await fetch_nationalize_data(name)

        processed_data = process_responses(
        name,
        agify_data,
        genderize_data,
        nationalize_data
    )
        db_profile = Profile(**processed_data)
        db.add(db_profile)
        db.commit()
        db.refresh(db_profile)

        return db_profile
