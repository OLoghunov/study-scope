from datetime import timedelta, datetime

from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import getSession
from src.db.models import User
from .schemas import (
    UserCreateModel,
    UserModel,
    UserLoginModel,
    UserBooksModel,
    EmailModel,
)
from .service import UserService
from .utils import (
    createAccessToken,
    verifyPassword,
    createUrlSafeToken,
    decodeUrlSafeToken,
)
from .dependencies import (
    RefreshTokenBearer,
    AccessTokenBearer,
    getCurrentUser,
    RoleChecker,
)
from src.db.redis import addJtiToBlocklist
from src.errors import UserAlreadyExists, InvalidCredentials, InvalidToken, UserNotFound
from src.mail import mail, createMessage
from src.config import Config

authRouter = APIRouter()
userService = UserService()
roleChecker = RoleChecker(["admin", "user"])

REFRESH_TOKEN_EXPIRY = 2


@authRouter.get("/verify/{token}")
async def verifyUserAccount(token: str, session: AsyncSession = Depends(getSession)):
    tokenData: dict = decodeUrlSafeToken(token)
    userEmail = tokenData.get("email")

    if userEmail:
        user = await userService.getUserByEmail(userEmail, session)
        if not user:
            raise UserNotFound()

        await userService.updateUser(user, {"isVerified": True}, session)
        return JSONResponse(
            content={"message": "Account verified succsessfully"},
            status_code=status.HTTP_200_OK,
        )
    return JSONResponse(
        content={"message": "Error occured during verification"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


@authRouter.post("/signup", status_code=status.HTTP_201_CREATED)
async def createUserAccount(
    userData: UserCreateModel, session: AsyncSession = Depends(getSession)
):
    email = userData.email
    userExists = await userService.userExists(email, session)

    if userExists:
        raise UserAlreadyExists()

    newUser = await userService.createUser(userData, session)

    token = createUrlSafeToken({"email": email})

    link = f"http://{Config.DOMAIN}/api/0.1/auth/verify/{token}"

    htmlMessage = f"""
    <p>Please click this <a href="{link}"> link</a> to verify your email</p>
    """

    message = createMessage(
        recipients=[email], subject="Verify Your Email", body=htmlMessage
    )

    await mail.send_message(message)

    return {
        "message": "Account created. Check email to verify your account",
        "user": newUser,
    }


@authRouter.post("/login")
async def loginUsers(
    loginData: UserLoginModel, session: AsyncSession = Depends(getSession)
):
    email = loginData.email
    password = loginData.password
    user: User = await userService.getUserByEmail(email, session)

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
