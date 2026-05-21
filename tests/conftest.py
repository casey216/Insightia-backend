import pytest

from fastapi.testclient import TestClient

from src.app import app
from src.api.db import database as db_module


@pytest.fixture(scope="function", autouse=True)
def setup_db():
    db_module.init_db(test=True)
    db_module.Base.metadata.create_all(bind=db_module.engine)

    yield

    db_module.Base.metadata.drop_all(bind=db_module.engine)


@pytest.fixture()
def db_session(setup_db):
    db = db_module.SessionLocal()

    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[db_module.get_db] = override_get_db
    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def mock_external_api_calls(monkeypatch):
    def _mock(agify_data=None, genderize_data=None, nationalize_data=None):
        async def fetch_agify_data(name):
            return agify_data or {"count": 147558, "name": name, "age": 74}

        async def fetch_genderize_data(name):
            return genderize_data or {
                "count": 1458986,
                "name": name,
                "gender": "male",
                "probability": 1,
            }

        async def fetch_nationalize_data(name):
            return nationalize_data or {
                "count": 311532,
                "name": name,
                "country": [
                    {"country_id": "US", "probability": 0.0873351111451966}
                ],
            }

        async def fetch_country_data(name):
            return {"name": "Nigeria"}

        monkeypatch.setattr(
            "src.api.v1.services.profile.fetch_agify_data",
            fetch_agify_data,
        )

        monkeypatch.setattr(
            "src.api.v1.services.profile.fetch_genderize_data",
            fetch_genderize_data,
        )

        monkeypatch.setattr(
            "src.api.v1.services.profile.fetch_nationalize_data",
            fetch_nationalize_data,
        )

        monkeypatch.setattr(
            "src.api.v1.services.profile.fetch_country_data",
            fetch_country_data,
        )

    return _mock
