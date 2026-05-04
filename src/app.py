from fastapi import FastAPI

from src.api.router import router


app = FastAPI(
    title="Insightia",
)
app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "welcome to Insightia." 
    }


@app.get("/health-check")
def health_check():
    return {
        "health": "ok"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app="src.app:app", reload=True)