from typing import Any

from src.core.exceptions import ExternalApiError


def process_genderize_response(data: dict[str, Any]) -> dict[str, Any]:
    gender: str = data.get("gender", "")
    gender_probability: float = round(data.get("probability", 0),2)
    sample_size: int = data.get("count", 0)

    if gender == "" or sample_size == 0:
        raise ExternalApiError("Genderize")

    return {
        "gender": gender,
        "gender_probability": gender_probability,
        "sample_size": sample_size,
    }


def classify_age_group(age: int) -> str:
    if age < 0:
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

    if not age:
        raise ExternalApiError("Agify")

    return {
        "age": age,
        "age_group": classify_age_group(age)
    }


def process_nationalize_response(data: dict[str, Any]) -> dict[str, Any]:
    try:
        country: dict = data.get("country", [])[0]
    except IndexError:
        raise ExternalApiError("Nationalize")

    return {
        "country_id": country.get("country_id", "").upper(),
        "country_probability": round(country.get("probability", 0), 2)
    }


def process_responses(name: str, agify_data: dict, genderize_data: dict, nationalize_data: dict) -> dict[str, Any]:
    result = {
        "name": name,
        }

    result.update(process_genderize_response(genderize_data))
    result.update(process_agify_response(agify_data))
    result.update(process_nationalize_response(nationalize_data))

    return result