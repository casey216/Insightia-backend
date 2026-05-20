import secrets
import uuid
from datetime import datetime, timedelta, timezone

from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from jose import jwt, JWSError
from jose.exceptions import ExpiredSignatureError
from sqlalchemy.orm import Session

from ..models.auth import RefreshToken
from src.api.core.exceptions import InvalidTokenError
from src.api.core.settings import settings
from src.api.v1.services.user import UserService


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
            raise InvalidTokenError("Token Expired.")
        except JWSError:
            raise InvalidTokenError("Invalid Token")
        
    @staticmethod
    def create_refresh_token(user_id: uuid.UUID, db: Session) -> str:
        token = str(uuid.uuid4())
        expires_at = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

        db_token = RefreshToken(
            token=token,
            user_id=user_id,
            expires_at=expires_at,
        )

        db.add(db_token)
        db.commit()

        return token
    
    @staticmethod
    def refresh_access_token(refresh_token: str, db: Session) -> tuple[str, str]:
        db_token = (
            db.query(RefreshToken)
            .filter(
                RefreshToken.token==refresh_token,
                RefreshToken.revoked==False,
                RefreshToken.expires_at>datetime.now(timezone.utc),
            ).first()
        )

        if not db_token:
            raise InvalidTokenError("Invalid or expired refresh token.")
        
        db_token.revoked = True
        db.commit()

        new_access_token = AuthService.create_jwt(
            db_token.user.to_dict(),
            settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        new_refresh_token = AuthService.create_refresh_token(db_token.user.id, db)

        return new_access_token, new_refresh_token
    
    @staticmethod
    def revoke_refresh_token(refresh_token: str, db: Session) -> None:
        db_token = db.query(RefreshToken).filter(RefreshToken.token==refresh_token).first()

        if db_token:
            db_token.revoked = True
            db.commit()
