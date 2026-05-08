from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from src.core.exceptions import ExternalApiError, InvalidIdError, ProfileNotFoundError


def add_exception_handlers(app: FastAPI):
    @app.exception_handler(HTTPException)
    def custom_http_exception_handler(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "status": "error",
                "message": exc.detail
            }
        )

    
    @app.exception_handler(ExternalApiError)
    def external_api_error_handler(request: Request, exc: ExternalApiError):
        return JSONResponse(
            status_code=502,
            content={
                "status": "error",
                "message": exc.detail
            }
        )


    @app.exception_handler(InvalidIdError)
    def invalid_id_error_handler(request: Request, exc: InvalidIdError):
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "message": exc.detail
            }
        )


    @app.exception_handler(ProfileNotFoundError)
    def profile_not_found_error_handler(request: Request, exc: ProfileNotFoundError):
        return JSONResponse(
            status_code=404,
            content={
                "status": "error",
                "message": exc.detail
            }
        )
