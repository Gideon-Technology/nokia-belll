from typing import Annotated, Optional

import jwt
from fastapi import Depends, Security
from fastapi.security import SecurityScopes, HTTPAuthorizationCredentials, HTTPBearer

from config import ClaimsApiConfig
from errors import UnauthenticatedRequest, UnauthorizedRequest


class VerifyToken:
    """Token authentication handler"""

    def __init__(self):
        config = ClaimsApiConfig.get_api_config()

        self._public_key = config.jwt_public_key

    async def verify(
        self,
        security_scopes: SecurityScopes,
        token: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer()),
    ):
        if token is None:
            raise UnauthenticatedRequest

        try:
            payload = jwt.decode(
                token.credentials,
                self._public_key,
                algorithms=["RS256"],
            )
        except Exception as error:
            raise UnauthorizedRequest(str(error))

        return payload


auth_scheme = VerifyToken()
auth_token_dependancy = Security(auth_scheme.verify)
AuthToken = Annotated[VerifyToken, auth_token_dependancy]
