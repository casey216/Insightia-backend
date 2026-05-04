from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from src.core.exceptions import ExternalApiError


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
