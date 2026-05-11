from typing import Literal, Annotated

from pydantic import BaseModel, BeforeValidator


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
