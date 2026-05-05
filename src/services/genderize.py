from typing import Any

import requests

from src.core.exceptions import ExternalApiError


GENDERIZE_URL = "https://api.genderize.io"


def fetch_name_data(name: str) -> dict[str, Any]:
    try:
        response = requests.get(
            url=GENDERIZE_URL,
            params={
                "name": name
            },
            timeout=2.0
        )
        response.raise_for_status()
    
    except requests.exceptions.RequestException as e:
        raise ExternalApiError() from e
    
    try:
        return response.json()
    except requests.exceptions.JSONDecodeError as e:
        raise ExternalApiError() from e
