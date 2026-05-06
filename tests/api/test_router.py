from fastapi.testclient import TestClient

from src.app import app
from src.core.exceptions import ExternalApiError


client = TestClient(app)


def test_success_case(monkeypatch):
    monkeypatch.setattr(
        "src.api.router.fetch_name_data", 
        lambda name : {
            "name": name,
            "gender": "male",
            "probability": 0.99,
            "count": 345678
        }
    )

    response = client.get("/api/classify?name=john")

    assert response.status_code == 200
    data = response.json()

    assert data["data"]["name"] == "john"
    assert data["data"]["processed_at"] is not None


def test_missing_name_returns_error(monkeypatch):
    response = client.get("/api/classify")

    assert response.status_code == 422


def test_empty_name_returns_400():
    response = client.get("/api/classify?name= ")
    
    assert response.status_code == 400
    assert response.json().get("message") == "Name cannot be empty"


def test_gender_is_null_and_count_is_zero_returns_400(monkeypatch):
    monkeypatch.setattr(
        "src.api.router.fetch_name_data",
        lambda name : {
            "name": name,
            "gender": None,
            "count": 0
        }
    )

    response = client.get("/api/classify?name=someinvalidname")

    assert response.status_code == 400
    assert response.json().get("message") == "No prediction available for the provided name"


def test_external_api_failure(monkeypatch):
    def fake_failure(name):
        raise ExternalApiError("API is down")

    monkeypatch.setattr(
        "src.api.router.fetch_name_data",
        fake_failure
    )

    response = client.get("/api/classify?name=john")

    assert response.status_code in [500, 502]
