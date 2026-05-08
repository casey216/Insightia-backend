from datetime import datetime, timezone
from typing import Any


def process_genderize_response(data: dict[str, Any]) -> dict[str, Any]:
    name: str = data.get("name", "")
    gender: str = data.get("gender", "")
    gender_probability: float = data.get("probability", 0)
    sample_size: int = data.get("count", 0)

    is_confident: bool = (gender_probability >= 0.7) and (sample_size >=100)

    return {
        "name": name.lower(),
        "gender": gender,
        "gender_probability": gender_probability,
        "sample_size": sample_size,
        "is_confident": is_confident,
        "processed_at": datetime.now(timezone.utc)
            .strftime("%Y-%m-%dT%H:%M:%SZ"),
    }


def classify_age_group(age: int | None) -> str:
    if age is None or age < 0:
        return "Invalid age"
    
    if age >= 0 and age < 13:
        return "child"
    
    if age < 20:
        return "teenager"
    
    if age < 60:
        return "adult"
    
    return "senior"


def process_agify_response(data: dict[str, Any]) -> dict[str, Any]:
    age = data.get("age")

    return {
        "age": age,
        "age_group": classify_age_group(age)
    }


def process_nationalize_response(data: dict[str, Any]) -> dict[str, Any]:
    country: dict = data.get("country", [])[0]

    return {
        "country_id": country.get("country_id"),
        "country_probability": country.get("probability")
    }