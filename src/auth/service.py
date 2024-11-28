from .models import User
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

        return True if user is not None else False

    async def createUser(self, userData: UserCreateModel, session: AsyncSession):
        userDataDict = userData.model_dump()
        newUser = User(**userDataDict)
        newUser.passwordHash = generatePasswordHash(userDataDict["password"])

        session.add(newUser)
        await session.commit()

        return newUser
