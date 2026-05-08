from typing import Any

import httpx

from src.core.exceptions import ExternalApiError


AGIFY_URL = "https://api.agify.io"


async def fetch_agify_data(name: str) -> dict[str, Any]:
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            response = await client.get(
                url=AGIFY_URL,
                params={
                    "name": name
                },
            )
        response.raise_for_status()
        
    except httpx.RequestError as e:
        raise ExternalApiError() from e
    
    except httpx.HTTPStatusError as e:
        raise ExternalApiError() from e
    
    try:
        return response.json()
    except ValueError as e:
        raise ExternalApiError() from e
