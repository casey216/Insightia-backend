from datetime import datetime, timezone
from typing import Any


def process_genderize_response(data: dict[str, Any]) -> dict[str, Any]:
    name = data.get("name")
    gender = data.get("gender")
    probability = data.get("probability", 0)
    sample_size = data.get("count", 0)

    is_confident = (probability >= 0.7) and (sample_size >=100)

    return {
        "name": name,
        "gender": gender,
        "probability": probability,
        "sample_size": sample_size,
        "is_confident": is_confident,
        "processed_at": datetime.now(timezone.utc)
            .strftime("%Y-%m-%dT%H:%M:%SZ"),
    }