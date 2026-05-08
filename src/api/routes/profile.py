from fastapi import APIRouter, HTTPException, Body

from src.schemas.profile import ProfileOut
from src.services.agify import fetch_agify_data
from src.services.genderize import fetch_genderize_data
from src.services.nationalize import fetch_nationalize_data
from src.utils.helpers import process_responses


router = APIRouter(prefix="/api/profiles", tags=["profiles"])


@router.post("/", response_model=ProfileOut, status_code=200)
async def get_name_details(name: str = Body(..., min_length=1, embed=True)):
    name = name.strip().lower()

    agify_data = await fetch_agify_data(name)
    genderize_data = await fetch_genderize_data(name)
    nationalize_data = await fetch_nationalize_data(name)

    if genderize_data.get("gender") is None or genderize_data.get("count") == 0:
        raise HTTPException(
            status_code=400,
            detail="No prediction available for the provided name"
        )

    processed_data = process_responses(
        name,
        agify_data,
        genderize_data,
        nationalize_data
    )

    return {
        "status": "success",
        "data": processed_data
    }
