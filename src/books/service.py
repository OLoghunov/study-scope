from datetime import datetime
import logging

from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import BookCreateModel, BookUpdateModel
from sqlmodel import select, desc
from src.db.models import Book


class BookService:
    async def getAllBooks(self, session: AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))
        result = await session.exec(statement)

        return result.all()

    async def getUserBooks(self, userUid: str, session: AsyncSession):
        statement = (
            select(Book).where(Book.userUid == userUid).order_by(desc(Book.created_at))
        )
        result = await session.exec(statement)
        
        return result.all()

    async def getBook(self, bookUid: str, session: AsyncSession):
        try:
            statement = select(Book).where(Book.uid == bookUid)
            result = await session.exec(statement)
        except Exception as e:
            logging.exception(e)
            return None

        return result.first()

    async def createBook(
        self, bookData: BookCreateModel, userUid: str, session: AsyncSession
    ):
        bookDataDict = bookData.model_dump()
        newBook = Book(**bookDataDict)
        newBook.published_date = datetime.strptime(
            bookDataDict["published_date"], "%Y-%m-%d"
        )
        newBook.userUid = userUid
        session.add(newBook)
        await session.commit()

        return newBook

    async def updateBook(
        self, bookUID: str, updateData: BookUpdateModel, session: AsyncSession
    ):
        bookToUpdate = await self.getBook(bookUID, session)

        if bookToUpdate is not None:
            updateDataDict = updateData.model_dump()
            updateDataDict["updated_at"] = datetime.now()

            for key, value in updateDataDict.items():
                setattr(bookToUpdate, key, value)

            await session.commit()

            return bookToUpdate
        else:
            return None

    async def deleteBook(self, bookUID: str, session: AsyncSession):
        bookToDelete = await self.getBook(bookUID, session)
        if bookToDelete is not None:
            await session.delete(bookToDelete)
            await session.commit()
            return {}
