from src.db.models import User
from .schemas import UserCreateModel
from .utils import generatePasswordHash
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select


class UserService:
    async def getUserByEmail(self, email: str, session: AsyncSession):
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)

        user = result.first()

        return user

    async def userExists(self, email: str, session: AsyncSession):
        user = await self.getUserByEmail(email, session)

        return user is not None

    async def createUser(self, userData: UserCreateModel, session: AsyncSession):
        userDataDict = userData.model_dump()
        newUser = User(**userDataDict)
        newUser.passwordHash = generatePasswordHash(userDataDict["password"])
        newUser.role = "user"

        session.add(newUser)
        await session.commit()

        return newUser

    async def updateUser(self, user: User, userData: dict, session: AsyncSession):
        for key, val in userData.items():
            setattr(user, key, val)

        await session.commit()

        return user
