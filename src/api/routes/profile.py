from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.schemas.profile import ProfileOut
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
