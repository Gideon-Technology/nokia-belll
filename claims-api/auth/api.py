import datetime as dt

from fastapi import APIRouter, Depends
import jwt
from pydantic import SecretStr

from config import AppConfigDependancy, config_dependancy
from errors import UnauthenticatedRequest, InternalError
from .models import LoginRequest, LoginResponse

auth_router = APIRouter(prefix="/auth", tags=["auth"], dependencies=[config_dependancy])


async def generate_token(
    username: str,
    secret_key: SecretStr,
    expiration: dt.datetime | None = None,
):
    audience = "api.claims.cool"
    issued_time = dt.datetime.now(tz=dt.timezone.utc)
    expires_at = expiration
    if expires_at is None:
        expires_at = issued_time + dt.timedelta(hours=8)
    jwt_payload = {
        "sub": username,
        "iss": f"{username}@{audience}",
        "iat": issued_time,
        "nbf": issued_time,
        "exp": expires_at,
    }
    token = jwt.encode(
        payload=jwt_payload, key=secret_key.get_secret_value(), algorithm="RS256"
    )
    return token


@auth_router.post("/login")
async def login(login_req: LoginRequest, api_config: AppConfigDependancy):
    token = await generate_token(
        username=login_req.username,
        secret_key=api_config.jwt_private_key,
    )
    return LoginResponse(token=token)
