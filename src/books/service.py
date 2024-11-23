from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import BookCreateModel, BookUpdateModel
from sqlmodel import select, desc
from .models import BookModel
from datetime import datetime


class BookService:
    async def getAllBooks(self, session: AsyncSession):
        statement = select(BookModel).order_by(desc(BookModel.created_at))
        result = await session.exec(statement)

        return result.all()

    async def getBook(self, bookUID: str, session: AsyncSession):
        statement = select(BookModel).where(BookModel.uid == bookUID)
        result = await session.exec(statement)
        
        return result.first()

    async def createBook(self, bookData: BookCreateModel, session: AsyncSession):
        bookDataDict = bookData.model_dump()
        newBook = BookModel(**bookDataDict)
        newBook.published_date = datetime.strptime(bookDataDict["published_date"], "%Y-%m-%d")
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
