from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from .exceptions import (
    ExternalApiError,
    InvalidIdError,
    ResourceNotFoundError,
    DuplicateResourceError,
    InvalidTokenError,
)


def add_exception_handlers(app: FastAPI):
    @app.exception_handler(HTTPException)
    def custom_http_exception_handler(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"status": "error", "message": exc.detail},
        )

    @app.exception_handler(ExternalApiError)
    def external_api_error_handler(request: Request, exc: ExternalApiError):
        return JSONResponse(
            status_code=502,
            content={"status": "error", "message": exc.detail},
        )

    @app.exception_handler(InvalidIdError)
    def invalid_id_error_handler(request: Request, exc: InvalidIdError):
        return JSONResponse(
            status_code=400,
            content={"status": "error", "message": exc.detail},
        )

    @app.exception_handler(ResourceNotFoundError)
    def profile_not_found_error_handler(
        request: Request, exc: ResourceNotFoundError
    ):
        return JSONResponse(
            status_code=404,
            content={"status": "error", "message": exc.detail},
        )

    @app.exception_handler(DuplicateResourceError)
    def duplicate_resource_exception_handler(
        request: Request, exc: DuplicateResourceError
    ):
        return JSONResponse(
            status_code=409,
            content={"status": "error", "message": exc.detail},
        )

    @app.exception_handler(InvalidTokenError)
    def invalid_token_error_handler(request: Request, exc: InvalidTokenError):

        return JSONResponse(
            status_code=401,
            content={"status": "error", "message": exc.detail},
        )

    @app.exception_handler(Exception)
    def internal_server_error_handler(request: Request, exc: Exception):

        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": "Internal server error"},
        )
