from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.schemas.profile import ProfileOut, FilterParams
from src.services.profile_service import ProfileService


router = APIRouter(prefix="/api/profiles", tags=["profiles"])


@router.post("/", response_model=ProfileOut, status_code=201)
async def create_profile(
            name: str = Body(..., min_length=1, embed=True),
            db: Session = Depends(get_db),

):
    name = name.strip().lower()
    processed_data = await ProfileService.create_profile(name, db)
    return {
        "status": "success",
        "data": processed_data.to_dict()
    }


@router.get("/{id}", response_model=ProfileOut, status_code=200)
async def get_profile(id: str, db: Annotated[Session, Depends(get_db)]):
    profile = ProfileService.get_profile_by_id(id, db)

    return {
        "status": "success",
        "data": profile.to_dict()
    }


@router.get("/", status_code=200)
async def get_all_profiles(filter_params: Annotated[FilterParams, Depends()], db: Annotated[Session, Depends(get_db)]):
    result = ProfileService.get_all_profiles(filter_params, db)

    return {
        "status": "success",
        "count": result.get("total"),
        "data": result.get("data")
    }


@router.delete("/id", status_code=204)
async def delete_profile(id: str, db: Annotated[Session, Depends(get_db)]):
    ProfileService.delete_profile(id, db)
    return
