from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes.profile import router
from src.db import database as db_module
from src.core.exception_handlers import add_exception_handlers
from src.core.settings import settings
from src.models.profile import Profile


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_module.init_db()
    db_module.Base.metadata.create_all(bind=db_module.engine)

    yield



app = FastAPI(
    title=settings.API_NAME,
    version=settings.API_VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_credentials=False,
    allow_headers=["*"]
)

app.include_router(router)
add_exception_handlers(app)


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
    reload = False
    if settings.ENV == "development": reload = True
    uvicorn.run(app="src.app:app", reload=reload)
