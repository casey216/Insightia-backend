from typing import Literal, Annotated

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field

from src.models.profile import Profile


Gender = Annotated[Literal["male", "female"], BeforeValidator(lambda x: x.lower())]
AgeGroup = Annotated[Literal["child", "teenager", "adult", "senior"], 
                     BeforeValidator(lambda x: x.lower())]


class ProfileData(BaseModel):
    id: str
    name: str
    gender: str
    gender_probability: float
    age: int
    age_group: str
    country_id: str
    country_name: str
    country_probability: float
    created_at: str


class ProfileOut(BaseModel):
    status: str
    message: str | None = None
    data: ProfileData


class ProfileCreate(BaseModel):
    name: str
    gender: str
    gender_probability: float
    age: int
    age_group: str
    country_id: str
    country_name: str
    country_probability: float


class FilterParams(BaseModel):
    gender: Gender | None = None
    age_group: AgeGroup | None = None
    country_id: str | None = None
    min_age: int | None = Field(None, gt=0)
    max_age: int | None = Field(None, gt=0)
    min_gender_probability: float | None = Field(None, ge=0.0, le=1.0)
    min_country_probability: float | None = Field(None, ge=0.0, le=1.0)


class SortParams(BaseModel):
    sort_by: Literal["age", "created_at", "gender_probability"] | None = None
    order: Literal["asc", "desc"] | None = None


class PaginationParams:
    def __init__(self, page: int = 1, limit: int = 10):
        self.page = max(1, page)
        self.limit = min(limit, 50)


    @property
    def offset(self):
        return (self.page - 1) * self.limit
    

class PaginatedResult(BaseModel):
    items: list[Profile]
    page: int
    limit: int
    total: int

    model_config = ConfigDict(arbitrary_types_allowed=True)
