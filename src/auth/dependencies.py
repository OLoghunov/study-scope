from fastapi import Request, status
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi.exceptions import HTTPException
from .utils import decodeToken
import logging

logger = logging.getLogger(__name__)


class AccessTokenBearer(HTTPBearer):

    def __init__(self, autoError=True):
        super().__init__(auto_error=autoError)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)

        token = creds.credentials

        tokenData = decodeToken(token)

        if not self.tokenValid(token):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Invalid or token"
            )

        if tokenData["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide an access token"
            )

        return tokenData

    def tokenValid(self, token: str) -> bool:
        tokenData = decodeToken(token)

        return True if tokenData is not None else False
