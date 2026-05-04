from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse


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
    