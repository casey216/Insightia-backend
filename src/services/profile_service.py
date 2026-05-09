import typing
import uuid

from sqlalchemy.orm import Session, Query
from sqlalchemy.exc import IntegrityError

from src.core.exceptions import InvalidIdError, ProfileNotFoundError, DuplicateResourceError
from src.models.profile import Profile
from src.schemas.profile import FilterParams
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

        try:
            db.add(db_profile)
            db.commit()
            db.refresh(db_profile)
            return db_profile
        except IntegrityError:
            db.rollback()
            raise DuplicateResourceError("Profile")
    

    @staticmethod
    def get_profile_by_id(id: str, db: Session) -> Profile:
        try:
            db_profile = db.query(Profile).filter_by(id=uuid.UUID(id)).first()
            if db_profile is None:
                raise ProfileNotFoundError()
        except ValueError as e:
            raise InvalidIdError
        return db_profile
    

    @staticmethod
    def get_profile_by_name(name: str, db: Session) -> Profile | None:
        return db.query(Profile).filter(Profile.name == name).first()
    

    @staticmethod
    def delete_profile(id: str, db: Session) -> None:
        db_profile = ProfileService.get_profile_by_id(id, db)
        db.delete(db_profile)
        db.commit()


    @staticmethod
    def get_all_profiles(filter_params: FilterParams, db: Session) -> dict[str, typing.Any]:
        q = QueryBuilder(db.query(Profile))
        q = q.filter_by_age(filter_params.age)
        q = q.filter_by_country(filter_params.country_id)
        q = q.filter_by_gender(filter_params.gender)
        q = q.build()

        count = q.count()
        profiles = [
            profile.to_dict()
            for profile in q.all()
        ]

        return {
            "total": count,
            "data": profiles
        }


class QueryBuilder:
    def __init__(self, query: Query[Profile]) -> None:
        self.query = query


    def filter_by_gender(self, gender: str | None):
        if gender:
            self.query = self.query.filter(Profile.gender == gender.lower())
        return self


    def filter_by_age(self, age: int | None):
        if age:
            self.query = self.query.filter(Profile.age == age)
        return self


    def filter_by_country(self, country_id: str | None):
        if country_id:
            self.query = self.query.filter(Profile.country_id == country_id.upper())
        return self


    def build(self) -> Query[Profile]:
        return self.query
