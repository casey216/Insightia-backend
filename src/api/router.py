from fastapi import APIRouter, HTTPException, Query

from src.services.genderize import fetch_name_data
from src.utils.helpers import process_genderize_response


router = APIRouter(prefix="/api")


@router.get("/classify")
async def get_name_details(name: str = Query(None)):
    if not name or name.strip() == "":
        raise HTTPException(
            status_code=400, 
            detail="Missing or empty name")
    
    raw_data = fetch_name_data(name.strip())

    processed_data = process_genderize_response(raw_data)
    return {
        "status": "success",
        "data": processed_data
    }
