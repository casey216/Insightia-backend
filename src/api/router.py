from fastapi import APIRouter, HTTPException, Query

from src.services.genderize import fetch_name_data


router = APIRouter(prefix="/api")


@router.get("/classify")
async def get_name_details(name: str = Query(None)):
    if not name or name.strip() == "":
        raise HTTPException(
            status_code=400, 
            detail="Missing or empty name")
    
    try:
        data = fetch_name_data(name.strip())
        return {
            "status": "success",
            "data": data
        }
    
    except Exception:
        raise HTTPException(
            status_code=502,
            detail="External API Error"
        )
