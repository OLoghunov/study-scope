from fastapi import Request, status
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi.exceptions import HTTPException
from .utils import decodeToken


class TokenBearer(HTTPBearer):

    def __init__(self, autoError=True):
        super().__init__(auto_error=autoError)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)

        token = creds.credentials

        tokenData = decodeToken(token)

        if not self.tokenValid(token):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or expired token"
            )

        self.verifyTokenData(tokenData)

        return tokenData

    def tokenValid(self, token: str) -> bool:
        tokenData = decodeToken(token)

        return True if tokenData is not None else False
    
    def verifyTokenData(self, tokenData: dict):
        raise NotImplementedError("Please Override this method in child classes")
        


class AccessTokenBearer(TokenBearer):

    def verifyTokenData(self, tokenData: dict) -> None:
        if tokenData and tokenData["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide an access token",
            )


class RefreshTokenBearer(TokenBearer):

    def verifyTokenData(self, tokenData: dict) -> None:
        if tokenData and not tokenData["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide a refresh token",
            )
