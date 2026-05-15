import json
from pathlib import Path

from src.api.db import database as db_module
from src.api.v1.models.profile import Profile


BASE_DIR = Path(__file__).resolve().parent
SEED_FILE = "seed_profiles.json"
SEED_PATH = f"{BASE_DIR}/{SEED_FILE}"


db_module.init_db()
db = db_module.SessionLocal()


def seed_profiles():
    with open(SEED_PATH, "r", encoding="utf-8") as file:
        raw = json.load(file)

        data = raw.get("profiles")

        for item in data:
            profile = Profile(**item)
            db.add(profile)
            try:
                db.commit()
            except Exception as e:
                print(f"Error {e} occured!")


if __name__ == "__main__":
    seed_profiles()
