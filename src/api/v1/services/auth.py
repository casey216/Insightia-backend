import secrets
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from jose import jwt, JWSError
from jose.exceptions import ExpiredSignatureError

from src.api.core.settings import settings


serializer = URLSafeTimedSerializer(settings.SECRET_KEY)


class AuthService:
    """Handles all business logic for user authentication"""

    @staticmethod
    def create_state_token(session_id: str):
        payload = {
            "sid": session_id,
            "nonce": secrets.token_urlsafe(16)
        }

        return serializer.dumps(
            payload,
            salt="oauth-state"
        )
    
    @staticmethod
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
    
    @staticmethod
    def create_jwt(data: dict, expires_delta_minutes: int):
        iat = datetime.now(timezone.utc)
        exp = iat + timedelta(minutes=expires_delta_minutes)
        payload = {
            **data,
            "iat": iat,
            "exp": exp
        }
        return jwt.encode(
            payload,
            key=settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )
    
    @staticmethod
    def verify_jwt(token: str):
        try:
            return jwt.decode(
                token=token,
                key=settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
        except ExpiredSignatureError:
            raise HTTPException(
                401,
                detail="Token expired"
            )
        except JWSError:
            raise HTTPException(
                401,
                detail="Invalid Token"
            )