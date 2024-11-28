from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import getSession
from .schemas import UserCreateModel, UserModel
from .service import UserService

authRouter = APIRouter()
service = UserService()


@authRouter.post(
    "/signup", response_model=UserModel, status_code=status.HTTP_201_CREATED
)
async def createUserAccount(
    userData: UserCreateModel, session: AsyncSession = Depends(getSession)
):
    email = userData.email
    userExists = await service.userExists(email, session)

    if userExists:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User with email {email} already exists",
        )

    newUser = await service.createUser(userData, session)

    return newUser
