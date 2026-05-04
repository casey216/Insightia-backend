from fastapi import APIRouter, HTTPException, Query


router = APIRouter(prefix="/api")


@router.get("/classify")
def get_name_details(name: str = Query(None)):
    if not name or name.strip() == "":
        raise HTTPException(400, "Missing or empty name")
    
    name = name.strip()
    
    return {
        "name": name
    }