from typing import Any

import httpx

from src.api.core.exceptions import ExternalApiError


API_URL = "https://www.apicountries.com/alpha"


async def fetch_country_data(country_id: str) -> dict[str, Any]:
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            response = await client.get(url=f"{API_URL}/{country_id}")
        response.raise_for_status()

    except httpx.RequestError as e:
        raise ExternalApiError() from e

    except httpx.HTTPStatusError as e:
        raise ExternalApiError() from e

    try:
        return response.json()
    except ValueError as e:
        raise ExternalApiError() from e
