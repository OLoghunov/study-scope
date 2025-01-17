from datetime import timedelta, datetime

from fastapi import APIRouter, status, Depends 
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import getSession
from src.db.models import User
from .schemas import UserCreateModel, UserModel, UserLoginModel, UserBooksModel
from .service import UserService
from .utils import createAccessToken, verifyPassword
from .dependencies import (
    RefreshTokenBearer,
    AccessTokenBearer,
    getCurrentUser,
    RoleChecker,
)
from src.db.redis import addJtiToBlocklist
from src.errors import (
    UserAlreadyExists,
    InvalidCredentials,
    InvalidToken
)

authRouter = APIRouter()
service = UserService()
roleChecker = RoleChecker(["admin", "user"])

REFRESH_TOKEN_EXPIRY = 2


@authRouter.post(
    "/signup", response_model=UserModel, status_code=status.HTTP_201_CREATED
)
async def createUserAccount(
    userData: UserCreateModel, session: AsyncSession = Depends(getSession)
):
    email = userData.email
    userExists = await service.userExists(email, session)

    if userExists:
        raise UserAlreadyExists()

    newUser = await service.createUser(userData, session)

    return newUser


@authRouter.post("/login")
async def loginUsers(
    loginData: UserLoginModel, session: AsyncSession = Depends(getSession)
):
    email = loginData.email
    password = loginData.password
    user: User = await service.getUserByEmail(email, session)

    if user is not None:
        passwordValid = verifyPassword(password, user.passwordHash)

        if passwordValid:
            accessToken = createAccessToken(
                userData={"email": email, "userUid": str(user.uid), "role": user.role}
            )

            refreshToken = createAccessToken(
                userData={"email": email, "userUid": str(user.uid)},
                refresh=True,
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY),
            )

            return JSONResponse(
                content={
                    "message": "Login successful",
                    "access_token": accessToken,
                    "refresh_token": refreshToken,
                    "user": {"email": user.email, "uid": str(user.uid)},
                }
            )

    raise InvalidCredentials()


@authRouter.get("/refresh_token")
async def getNewAccessToken(tokenDetails: dict = Depends(RefreshTokenBearer())):
    expiryTimestamp = tokenDetails["exp"]

    if datetime.fromtimestamp(expiryTimestamp) > datetime.now():
        newAccessToken = createAccessToken(userData=tokenDetails["user"])

        return JSONResponse(content={"access_token": newAccessToken})

    raise InvalidToken()


@authRouter.get("/me", response_model=UserBooksModel)
async def getCurrentUser(user=Depends(getCurrentUser), _: bool = Depends(roleChecker)):
    return user


@authRouter.get("/logout")
async def revokeToken(tokenDetails: dict = Depends(AccessTokenBearer())):
    jti = tokenDetails["jti"]

    await addJtiToBlocklist(jti)

    return JSONResponse(
        content={"message": "Logged out successfully"}, status_code=status.HTTP_200_OK
    )
