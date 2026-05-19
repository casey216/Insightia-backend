import uuid

from sqlalchemy import asc, desc
from sqlalchemy.orm import Session, Query
from sqlalchemy.exc import IntegrityError

from src.api.core.exceptions import (
    InvalidIdError,
    ResourceNotFoundError,
    DuplicateResourceError,
)
from src.api.v1.models.profile import Profile
from src.api.v1.schemas.profile import (
    FilterParams,
    SortParams,
    PaginationParams,
    PaginatedResult,
)
from src.api.v1.services.agify import fetch_agify_data
from src.api.v1.services.api_countries import fetch_country_data
from src.api.v1.services.genderize import fetch_genderize_data
from src.api.v1.services.nationalize import fetch_nationalize_data
from src.api.utils.helpers import process_responses


class ProfileService:
    """Service layer business logic for profiles."""

    @staticmethod
    async def create_profile(name: str, db: Session) -> Profile:
        agify_data = await fetch_agify_data(name)
        genderize_data = await fetch_genderize_data(name)
        nationalize_data = await fetch_nationalize_data(name)

        processed_data = process_responses(
            name, agify_data, genderize_data, nationalize_data
        )

        country_data = await fetch_country_data(
            processed_data.get("country_id", "")
        )
        country_name = country_data.get("name")
        processed_data["country_name"] = country_name

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
                raise ResourceNotFoundError("Profile")
        except ValueError:
            raise InvalidIdError(f"Profile")
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
    def get_all_profiles(
        filter_params: FilterParams,
        sort_params: SortParams,
        pagination_params: PaginationParams,
        db: Session,
    ) -> PaginatedResult:
        q = (
            QueryBuilder(db.query(Profile))
            .filter_by_age_group(filter_params.age_group)
            .filter_by_country(filter_params.country_id)
            .filter_by_gender(filter_params.gender)
            .filter_by_age(filter_params.min_age, filter_params.max_age)
            .filter_by_gender_probability(filter_params.min_gender_probability)
            .filter_by_country_probability(
                filter_params.min_country_probability
            )
            .sort_by(sort_params)
        )

        total = q.count()

        profiles = q.paginate(pagination_params).build().all()

        return PaginatedResult(
            items=profiles,
            page=pagination_params.page,
            limit=pagination_params.limit,
            total=total,
        )


class QueryBuilder:
    def __init__(self, query: Query[Profile]) -> None:
        self.query = query
        self.sort_columns = {
            "age": Profile.age,
            "created_at": Profile.created_at,
            "gender_probability": Profile.gender_probability,
        }

    def filter_by_gender(self, gender: str | None):
        if gender:
            self.query = self.query.filter(Profile.gender == gender)
        return self

    def filter_by_age_group(self, age_group: str | None):
        if age_group:
            self.query = self.query.filter(Profile.age_group == age_group)
        return self

    def filter_by_country(self, country_id: str | None):
        if country_id:
            self.query = self.query.filter(
                Profile.country_id == country_id.upper()
            )
        return self

    def filter_by_age(self, min_age: int | None, max_age: int | None):
        if min_age:
            self.query = self.query.filter(Profile.age >= min_age)
        if max_age:
            self.query = self.query.filter(Profile.age <= max_age)

        return self

    def filter_by_gender_probability(
        self, min_gender_probability: float | None
    ):
        if min_gender_probability:
            self.query = self.query.filter(
                Profile.gender_probability >= min_gender_probability
            )
        return self

    def filter_by_country_probability(
        self, min_country_probability: float | None
    ):
        if min_country_probability:
            self.query = self.query.filter(
                Profile.country_probability >= min_country_probability
            )
        return self

    def sort_by(self, sort_params: SortParams):
        sort_column = (
            self.sort_columns.get(sort_params.sort_by)
            if sort_params.sort_by
            else None
        )

        if sort_column is None:
            self.query = self.query.order_by(asc(Profile.created_at))
            return self

        order_fn = desc if sort_params.order == "desc" else asc
        self.query = self.query.order_by(order_fn(sort_column))
        return self

    def paginate(self, pagination_params: PaginationParams):
        self.query = self.query.offset(pagination_params.offset).limit(
            pagination_params.limit
        )
        return self

    def count(self) -> int:
        return self.query.count()

    def build(self) -> Query[Profile]:
        return self.query
