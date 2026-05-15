import secrets

from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

from src.api.core.settings import settings


serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
router = APIRouter(prefix="/auth", tags=["authentication"])


def create_state_token(session_id: str):
    payload = {
        "sid": session_id,
        "nonce": secrets.token_urlsafe(16)
    }

    return serializer.dumps(
        payload,
        salt="oauth-state"
    )


def verify_state_token(token: str, session_id: str):
    try:
        payload = serializer.loads(
            token,
            salt="oauth-state",
            max_age=settings.CSRF_MAX_AGE_SECONDS
        )
    except SignatureExpired:
        return False
    except BadSignature:
        return False
    
    return secrets.compare_digest(
        payload["sid"],
        session_id
    )


@router.get("/github")
async def login(request: Request):
    session_id = request.cookies.get("session_id")
    if not session_id:
        session_id = secrets.token_urlsafe(32)

    oauth_state = create_state_token(session_id)

    url = (
        f"{settings.GITHUB_AUTHORIZE_URL}"
        f"?client_id={settings.GITHUB_CLIENT_ID}"
        f"&state={oauth_state}"
    )

    response = RedirectResponse(url)

    response.set_cookie(
        key="session_id",
        value=session_id,
        max_age=settings.CSRF_MAX_AGE_SECONDS,
        secure=False,
        httponly=True,
        samesite='lax',
    )

    return response