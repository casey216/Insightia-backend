import requests


GENDERIZE_URL = "https://api.genderize.io"


def fetch_name_data(name: str) -> requests.Response:
    response = requests.get(
        url=GENDERIZE_URL,
        params={
            "name": name
        },
        timeout=2.0
    )

    if response.status_code != 200:
        raise Exception("API Failure")
    
    return response.json()