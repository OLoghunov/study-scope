from sqlmodel import create_engine, SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine
from src.config import Config
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker


asyncEngine = AsyncEngine(create_engine(url=Config.DATABASE_URL, echo=True))


async def initDb() -> None:
    async with asyncEngine.begin() as conn:
        from src.books.models import Book

        await conn.run_sync(SQLModel.metadata.create_all)


async def getSession():
    Session = sessionmaker(
        bind=asyncEngine, class_=AsyncSession, expire_on_commit=False
    )

    async with Session() as session:
        yield session
