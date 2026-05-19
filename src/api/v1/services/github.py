import httpx

from src.api.core.settings import settings


async def exchange_code_for_token(code: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            settings.GITHUB_TOKEN_URL,
            headers={"Accept": "application/json"},
            data={
                "client_id": settings.GITHUB_CLIENT_ID,
                "client_secret": settings.GITHUB_CLIENT_SECRET,
                "code": code,
            },
        )
        return response.json()
    

async def get_github_user(token: str):
    headers={
        "Authorization": f"Bearer {token}"
        }
    async with httpx.AsyncClient() as client:
        user_res = await client.get(
            settings.GITHUB_USER_URL,
            headers=headers
        )
        email_res = await client.get(
            settings.GITHUB_EMAIL_URL,
            headers=headers
        )
        user = user_res.json()
        result = {
            "github_id": str(user.get("id")),
            "username": user.get("login"),
            "avatar_url": user.get("avatar_url")
        }
        for email in email_res.json():
            if email.get("verified") and email.get("primary"):
                result["email"] = email.get("email")
        return result    
