from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.schemas.profile import ProfileOut, FilterParams
from src.services.profile_service import ProfileService


router = APIRouter(prefix="/api/profiles", tags=["profiles"])


@router.post("/", response_model=ProfileOut, response_model_exclude_none=True)
async def create_profile(
            response: Response,
            name: str = Body(None, embed=True),
            db: Session = Depends(get_db),

):
    if name is None or name.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="Missing or empty name."
        )
    
    name = name.strip().lower()
    existing = ProfileService.get_profile_by_name(name, db)
    if existing:
        response.status_code = 200
        return {
            "status": "success",
            "message": "Profile already exists",
            "data": existing.to_dict()
        }
    processed_data = await ProfileService.create_profile(name, db)
    response.status_code = 201
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
