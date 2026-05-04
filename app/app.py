from fastapi import FastAPI


app = FastAPI(
    title="Insightia",
)


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
    uvicorn.run(app="app:app", reload=True)