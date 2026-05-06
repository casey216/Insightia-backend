from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse


class EmptyNameMiddleware(BaseHTTPMiddleware):
    "Return status code 400 for missing name query"

    async def dispatch(self, request: Request, call_next) -> Response:
        if request.query_params.get("name") is None:
            return JSONResponse(
                status_code=400,
                content={
                "status": "error",
                "message": "Missing or empty name"
                }
            )
        
        response = await call_next(request)
        return response
