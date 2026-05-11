# Insightia Backend

A **Profile Intelligence Service** built with FastAPI and PostgreSQL. Given a name, it enriches it with predicted gender, age, and nationality data by concurrently querying three external APIs, then stores and exposes the result through a clean RESTful interface.

---

## Table of Contents

- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Variables](#environment-variables)
  - [Running the Server](#running-the-server)
- [Database Options](#database-options)
- [API Reference](#api-reference)
  - [POST /api/profiles](#post-apiprofiles)
  - [GET /api/profiles](#get-apiprofiles)
  - [GET /api/profiles/{id}](#get-apiprofilesid)
  - [DELETE /api/profiles/{id}](#delete-apiprofilesid)
- [Error Handling](#error-handling)
- [Running Tests](#running-tests)

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| Server | Uvicorn |
| ORM | SQLAlchemy 2.0 |
| Database | PostgreSQL (production), SQLite (dev/test) |
| Validation | Pydantic v2 |
| HTTP Client | HTTPX (async) |
| IDs | UUID v7 (`uuid7`) |
| Settings | pydantic-settings |

---

## Project Structure

```
Insightia-backend/
├── src/
│   ├── app.py                   # FastAPI app, middleware, lifespan
│   ├── api/
│   │   └── routes/
│   │       └── profile.py       # Route handlers for /api/profiles
│   ├── core/
│   │   ├── settings.py          # Env-based config (pydantic-settings)
│   │   ├── exceptions.py        # Custom exception classes
│   │   ├── exception_handlers.py# Global exception → HTTP response mapping
│   │   └── middleware.py        # EmptyNameMiddleware
│   ├── db/
│   │   └── database.py          # Engine setup, session factory, Base
│   ├── models/
│   │   ├── base.py              # BaseModel with to_dict() serialization
│   │   └── profile.py           # Profile SQLAlchemy model
│   ├── schemas/
│   │   └── profile.py           # Pydantic schemas (in/out/filters)
│   ├── services/
│   │   ├── profile_service.py   # Business logic, QueryBuilder
│   │   ├── agify.py             # Agify API client
│   │   ├── genderize.py         # Genderize API client
│   │   └── nationalize.py       # Nationalize API client
│   └── utils/
│       └── helpers.py           # Response processors, age classifier
└── tests/
    ├── conftest.py              # Fixtures: in-memory DB, test client, API mocks
    └── api/routes/
        └── test_profile.py      # Endpoint and edge case tests
```

---

## Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL (for production) or SQLite (for local development)
- `pip`

### Installation

```bash
# Clone the repository
git clone https://github.com/casey216/Insightia-backend.git
cd Insightia-backend

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate       # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Variables

Copy the sample file and fill in your values:

```bash
cp .env.sample .env
```

```env
# Database
DB_TYPE=postgres         # postgres | sqlite | vercel
DB_HOST=localhost
DB_PORT=5432
DB_USER=insightia
DB_PASSWORD=your_password
DB_NAME=insightia

# App
API_NAME=Insightia Labs
API_VERSION=1.0.0
ENV=development
```

> For local development without PostgreSQL, set `DB_TYPE=sqlite` and `DB_NAME=insightia` — this creates a `insightia.db` file locally with no further setup needed.

### Running the Server

```bash
python -m src.app
```

The API will be available at `http://localhost:8000`.

Interactive docs (Swagger UI): `http://localhost:8000/docs`

---

## Database Options

The app supports three database modes controlled by `DB_TYPE` in `.env`:

| `DB_TYPE` | Description |
|---|---|
| `postgres` | Full PostgreSQL — recommended for production |
| `sqlite` | Local file-based SQLite — good for development |
| `vercel` | SQLite at `/tmp/` — for Vercel serverless development deployments |

---

## API Reference

All endpoints return `Content-Type: application/json` and include the header `Access-Control-Allow-Origin: *`.

---

### POST /api/profiles

Create a new profile by enriching a name via the Genderize, Agify, and Nationalize APIs. If a profile with the same name already exists, the existing record is returned without creating a duplicate.

**Request body**

```json
{ "name": "ella" }
```

**Response — 201 Created** (new profile)

```json
{
  "status": "success",
  "data": {
    "id": "019606e4-3f1a-7c4a-b7b7-dc48d4b23481",
    "name": "ella",
    "gender": "female",
    "gender_probability": 0.99,
    "sample_size": 1234,
    "age": 46,
    "age_group": "adult",
    "country_id": "NG",
    "country_probability": 0.85,
    "created_at": "2026-05-11T12:00:00Z"
  }
}
```

**Response — 200 OK** (name already exists)

```json
{
  "status": "success",
  "message": "Profile already exists",
  "data": { "...existing profile fields..." }
}
```

---

### GET /api/profiles

Retrieve all profiles. Supports optional case-insensitive filtering via query parameters.

**Query parameters**

| Parameter | Type | Description |
|---|---|---|
| `gender` | string | Filter by gender (`male` or `female`) |
| `country_id` | string | Filter by country code (e.g. `NG`, `US`) |
| `age` | integer | Filter by exact age |

**Example**

```
GET /api/profiles?gender=female&country_id=NG
```

**Response — 200 OK**

```json
{
  "status": "success",
  "count": 1,
  "data": [
    {
      "id": "019606e4-3f1a-7c4a-b7b7-dc48d4b23481",
      "name": "ella",
      "gender": "female",
      "gender_probability": 0.99,
      "sample_size": 1234,
      "age": 46,
      "age_group": "adult",
      "country_id": "NG",
      "country_probability": 0.85,
      "created_at": "2026-05-11T12:00:00Z"
    }
  ]
}
```

---

### GET /api/profiles/{id}

Retrieve a single profile by its UUID v7 identifier.

**Example**

```
GET /api/profiles/019606e4-3f1a-7c4a-b7b7-dc48d4b23481
```

**Response — 200 OK**

```json
{
  "status": "success",
  "data": {
    "id": "019606e4-3f1a-7c4a-b7b7-dc48d4b23481",
    "name": "ella",
    "gender": "female",
    "gender_probability": 0.99,
    "sample_size": 1234,
    "age": 46,
    "age_group": "adult",
    "country_id": "NG",
    "country_probability": 0.85,
    "created_at": "2026-05-11T12:00:00Z"
  }
}
```

---

### DELETE /api/profiles/{id}

Delete a profile by its UUID v7 identifier.

**Example**

```
DELETE /api/profiles/019606e4-3f1a-7c4a-b7b7-dc48d4b23481
```

**Response — 204 No Content** (empty body)

---

## Error Handling

All errors follow a consistent structure:

```json
{
  "status": "error",
  "message": "<descriptive message>"
}
```

| HTTP Code | Trigger |
|---|---|
| `400` | Missing or empty `name` in request body; malformed UUID |
| `404` | Profile not found by the given `id` |
| `422` | Invalid type supplied for `name` (non-string) |
| `500` | Unexpected internal server error |
| `502` | Upstream API (Genderize, Agify, or Nationalize) returned an invalid or incomplete response |

**Example 502 response**

```json
{
  "status": "error",
  "message": "Agify returned an invalid response."
}
```

The upstream API that failed is always named explicitly in the message.

---

## Running Tests

Tests use an in-memory SQLite database and mock all three external API calls — no live network access is needed.

```bash
pytest
```

The test suite covers:

- Profile creation (201)
- Idempotency — duplicate name returns 200
- Retrieve by ID
- Retrieve all profiles
- Delete profile
- 502 edge cases for each external API (null age, null/missing gender, empty country array)