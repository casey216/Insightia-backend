from typing import Any

import httpx

from src.api.core.exceptions import ExternalApiError


GENDERIZE_URL = "https://api.genderize.io"


async def fetch_genderize_data(name: str) -> dict[str, Any]:
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            response = await client.get(
                url=GENDERIZE_URL,
                params={"name": name},
            )
        response.raise_for_status()
        return response.json()

    except httpx.RequestError as e:
        raise ExternalApiError() from e

    except httpx.HTTPStatusError as e:
        raise ExternalApiError() from e

    except ValueError as e:
        raise ExternalApiError() from e
