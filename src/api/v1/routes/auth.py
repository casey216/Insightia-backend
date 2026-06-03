import secrets
from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, Header, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from ..schemas.auth import RefreshToken, RefreshTokenOut
from ..services.auth import AuthService
from ..services.github import exchange_code_for_token, get_github_user
from ..services.user import UserService
from src.api.core.settings import settings
from src.api.db.database import get_db


router = APIRouter(prefix="/auth", tags=["authentication"])


@router.get("/github")
async def login():
    session_id = secrets.token_urlsafe(32)
    oauth_state = AuthService.create_state_token(session_id)

    url = (
        f"{settings.GITHUB_AUTHORIZE_URL}"
        f"?client_id={settings.GITHUB_CLIENT_ID}"
        f"&state={oauth_state}"
        f"&redirect_uri=http://127.0.0.1:8000/auth/github/callback"
    )

    response = RedirectResponse(url)
    response.set_cookie(
        key="session_id",
        value=session_id,
        max_age=settings.CSRF_MAX_AGE_SECONDS,
        secure=False,
        httponly=True,
        samesite="lax",
    )

    return response


@router.get("/github/callback")
async def handle_callback(
    db: Annotated[Session, Depends(get_db)],
    code: str | None = None,
    session_id: Annotated[str | None, Cookie()] = None,
    state: str | None = None
):
    if not session_id:
        raise HTTPException(status_code=400, detail="session cookie missing")

    if not code:
        raise HTTPException(
            status_code=400, detail="Missing 'code' parameter from Github"
        )

    if not state or not AuthService.verify_state_token(state, session_id):
        raise HTTPException(
            status_code=403,
            detail=(
                "CSRF validation failed: invalid or expired state parameter"
            ),
        )

    token_data = await exchange_code_for_token(code)
    github_access_token = token_data.get("access_token")
    if not github_access_token:
        raise HTTPException(400, "GitHub OAuth failed")

    user_data = await get_github_user(github_access_token)

    db_user = UserService.create(user_data, db)

    access_token = AuthService.create_jwt(
        db_user.to_dict(), settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    refresh_token = AuthService.create_refresh_token(db_user.id, db)

    response = RedirectResponse("/")

    response.set_cookie(
        key="access_token",
        value=access_token,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        secure=False,
        httponly=True,
        samesite="lax",
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        secure=False,
        httponly=True,
        samesite="lax",
    )

    return response


@router.post("/refresh", status_code=200, response_model=RefreshTokenOut)
async def refresh_access_token(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
    token: RefreshToken | None = None
):
    old_token = (
        token.refresh_token
        if token
        else request.cookies.get("refresh_token", "")
    )
    
    if not old_token:
        raise HTTPException(
            status_code=400,
            detail="Refresh token required"
        )
    
    access_token, refresh_token = (
        AuthService.refresh_access_token(old_token, db)
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }
