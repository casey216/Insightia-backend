from pydantic import BaseModel


class RefreshToken(BaseModel):
    refresh_token: str | None = None


class RefreshTokenOut(BaseModel):
    access_token: str
    refresh_token: str