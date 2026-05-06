# Insightia

A Python REST API that proxies the [Genderize.io](https://genderize.io) API, enriches the response with a confidence flag and UTC timestamp, and returns a standardised JSON payload.

🌐 **Live API:** [https://insightia-backend.vercel.app](https://insightia-backend.vercel.app)  
📖 **Interactive Docs:** [https://insightia-backend.vercel.app/docs](https://insightia-backend.vercel.app/docs)

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| [FastAPI](https://fastapi.tiangolo.com/) | Web framework & API routing |
| [Uvicorn](https://www.uvicorn.org/) | ASGI server |
| [Pydantic](https://docs.pydantic.dev/) | Data validation & serialisation |
| [HTTPX](https://www.python-httpx.org/) | Async HTTP client for upstream API calls |
| [Vercel](https://vercel.com/) | Deployment & hosting |

---

## Project Structure

```
Insightia-backend/
├── src/                  # Application source code
│   └── ...
├── tests/                # Test suite
│   └── ...
├── requirements.txt      # Pinned Python dependencies
└── .gitignore
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- `pip`

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/casey216/Insightia-backend.git
   cd Insightia-backend
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate        # macOS/Linux
   venv\Scripts\activate           # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

### Running the Development Server

```bash
uvicorn src.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

---

## API Reference

### `GET /api/classify`

Accepts a `name` query parameter, calls the Genderize.io API, and returns an enriched gender prediction payload.

#### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | ✅ Yes | The name to classify |

---

### Success Response — `200 OK`

```json
{
  "status": "success",
  "data": {
    "name": "james",
    "gender": "male",
    "probability": 0.99,
    "sample_size": 1234,
    "is_confident": true,
    "processed_at": "2026-05-06T10:30:00Z"
  }
}
```

#### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | Always `"success"` on a valid response |
| `data.name` | string | The queried name |
| `data.gender` | string | `"male"` or `"female"` |
| `data.probability` | float | Prediction confidence, `0.0` – `1.0` |
| `data.sample_size` | integer | Sample count from Genderize (renamed from `count`) |
| `data.is_confident` | boolean | `true` if `probability >= 0.7` **AND** `sample_size >= 100` |
| `data.processed_at` | string | UTC timestamp in ISO 8601 format, dynamically generated |

---

### Error Responses

All errors follow a uniform structure:

```json
{
  "status": "error",
  "message": "<descriptive error message>"
}
```

| Status Code | Trigger |
|-------------|---------|
| `400 Bad Request` | `name` parameter is missing or empty |
| `422 Unprocessable Entity` | `name` parameter is not a string |
| `500 / 502 Server Error` | Internal error or upstream Genderize API failure |

**Edge case** — if Genderize returns `gender: null` or `count: 0`, the endpoint responds with an error payload:

```json
{
  "status": "error",
  "message": "No prediction available for the provided name"
}
```

---

## Usage Examples

### cURL

```bash
# Valid request
curl "https://insightia-backend.vercel.app/api/classify?name=james"

# Missing name → 400
curl "https://insightia-backend.vercel.app/api/classify"

# Empty name → 400
curl "https://insightia-backend.vercel.app/api/classify?name="
```

### Python (httpx)

```python
import httpx

response = httpx.get(
    "https://insightia-backend.vercel.app/api/classify",
    params={"name": "james"}
)
print(response.json())
```

---

## Running Tests

```bash
pytest tests/
```

For verbose output:

```bash
pytest tests/ -v
```
