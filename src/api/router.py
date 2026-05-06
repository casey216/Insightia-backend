from fastapi import APIRouter, HTTPException, Query

from src.services.genderize import fetch_name_data
from src.utils.helpers import process_genderize_response


router = APIRouter(prefix="/api")


@router.get("/classify")
async def get_name_details(name: str = Query(..., min_length=1)):
    name = name.strip()
    if name == "":
        raise HTTPException(
            status_code=400, 
            detail="Name cannot be empty")
    
    raw_data = fetch_name_data(name)

    if raw_data.get("gender") is None or raw_data.get("count") == 0:
        raise HTTPException(
            status_code=400,
            detail="No prediction available for the provided name"
        )

    processed_data = process_genderize_response(raw_data)
    return {
        "status": "success",
        "data": processed_data
    }
