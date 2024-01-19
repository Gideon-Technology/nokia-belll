import datetime as dt

from fastapi import APIRouter

from auth import auth_token_dependancy
from clients import ClaimsDBClient
from config import AppConfigDependancy, config_dependancy
from errors import UnauthenticatedRequest, InternalError
from .models import GetClaimsResponse

claims_router = APIRouter(
    prefix="/claims",
    tags=["claims"],
    dependencies=[
        auth_token_dependancy,
        config_dependancy,
    ],
)


@claims_router.get("")
async def login(
    api_config: AppConfigDependancy,
    limit: int = 25,
):
    db = ClaimsDBClient(api_config)
    claims_records = db.get_claims(limit=limit)
    return GetClaimsResponse.model_validate({"claims": claims_records})
