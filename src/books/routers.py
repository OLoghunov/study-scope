from typing import List
from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.service import BookService
from src.books.schemas import BookModel, BookUpdateModel, BookCreateModel

from src.db.main import getSession


booksRouter = APIRouter()
BookService = BookService()


@booksRouter.get("/", response_model=List[BookModel])
async def getAllBooks(session: AsyncSession = Depends(getSession)):
    books = await BookService.getAllBooks(session)
    return books


@booksRouter.post("/", status_code=status.HTTP_201_CREATED, response_model=BookModel)
async def createBook(bookData: BookCreateModel, session: AsyncSession = Depends(getSession)):
    newBook = await BookService.createBook(bookData, session)
    return newBook


@booksRouter.get("/{book_uid}", response_model=BookModel)
async def getBookById(book_uid: str, session: AsyncSession = Depends(getSession)):
    book = await BookService.getBook(book_uid, session)
    if book:
        return book
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )


@booksRouter.patch("/{book_uid}", response_model=BookModel)
async def updateBookById(
    book_uid: str,
    update_data: BookUpdateModel,
    session: AsyncSession = Depends(getSession),
):
    updatedBook = await BookService.updateBook(book_uid, update_data, session)
    if updatedBook:
        return updatedBook
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@booksRouter.delete("/{book_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def deleteBookById(book_uid: str, session: AsyncSession = Depends(getSession)):
    deleted = await BookService.deleteBook(book_uid, session)
    if deleted is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")