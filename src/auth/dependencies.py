from typing import List

from fastapi import Request, status, Depends
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi.exceptions import HTTPException
from .utils import decodeToken
from src.db.redis import tokenInBlocklist
from src.db.main import getSession
from sqlmodel.ext.asyncio.session import AsyncSession
from .service import UserService
from .models import User


userService = UserService()


class TokenBearer(HTTPBearer):

    def __init__(self, autoError=True):
        super().__init__(auto_error=autoError)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)

        token = creds.credentials

        tokenData = decodeToken(token)

        if not self.tokenValid(token):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "This token is invalid or expired",
                    "resolution": "Please get new token",
                },
            )

        if await tokenInBlocklist(tokenData["jti"]):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "This token is invalid or has been revoked",
                    "resolution": "Please get new token",
                },
            )

        self.verifyTokenData(tokenData)

        return tokenData

    def tokenValid(self, token: str) -> bool:
        tokenData = decodeToken(token)

        return tokenData is not None

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


async def getCurrentUser(
    tokenDetails: dict = Depends(AccessTokenBearer()),
    session: AsyncSession = Depends(getSession),
):
    userEmail = tokenDetails["user"]["email"]

    user = await userService.getUserByEmail(userEmail, session)

    return user


class RoleChecker:
    def __init__(self, allowedRoles: List[str]) -> None:
        self.allowedRoles = allowedRoles

    def __call__(self, currentUser: User = Depends(getCurrentUser)):
        if currentUser.role in self.allowedRoles:
            return True
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Operation not permitted"
        )
