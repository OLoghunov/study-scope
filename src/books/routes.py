from typing import List
from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from .service import BookService
from .schemas import BookModel, BookUpdateModel, BookCreateModel, BookDetailModel
from src.auth.dependencies import AccessTokenBearer, RoleChecker

from src.db.main import getSession


booksRouter = APIRouter()
BookService = BookService()
accessTokenBearer = AccessTokenBearer()
roleChecker = Depends(RoleChecker(["admin", "user"]))


@booksRouter.get("/", response_model=List[BookModel], dependencies=[roleChecker])
async def getAllBooks(
    session: AsyncSession = Depends(getSession),
    tokenDetails: dict = Depends(accessTokenBearer),
):
    books = await BookService.getAllBooks(session)
    return books


@booksRouter.get("/user/{userUid}", response_model=List[BookModel], dependencies=[roleChecker])
async def getUserBooksSubmissions(
    userUid: str,
    session: AsyncSession = Depends(getSession),
    tokenDetails: dict = Depends(accessTokenBearer),
):
    books = await BookService.getUserBooks(userUid, session)
    return books


@booksRouter.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=BookModel,
    dependencies=[roleChecker],
)
async def createBook(
    bookData: BookCreateModel,
    session: AsyncSession = Depends(getSession),
    tokenDetails: dict = Depends(accessTokenBearer),
):
    userId = tokenDetails["user"]["userUid"]
    newBook = await BookService.createBook(bookData, userId, session)
    return newBook


@booksRouter.get("/{book_uid}", response_model=BookDetailModel, dependencies=[roleChecker])
async def getBookById(
    book_uid: str,
    session: AsyncSession = Depends(getSession),
    tokenDetails: dict = Depends(accessTokenBearer),
) -> dict:
    book = await BookService.getBook(book_uid, session)
    if book:
        return book
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )


@booksRouter.patch("/{book_uid}", response_model=BookModel, dependencies=[roleChecker])
async def updateBookById(
    book_uid: str,
    update_data: BookUpdateModel,
    session: AsyncSession = Depends(getSession),
    tokenDetails: dict = Depends(accessTokenBearer),
):
    updatedBook = await BookService.updateBook(book_uid, update_data, session)
    if updatedBook:
        return updatedBook
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )


@booksRouter.delete(
    "/{book_uid}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[roleChecker]
)
async def deleteBookById(
    book_uid: str,
    session: AsyncSession = Depends(getSession),
    tokenDetails: dict = Depends(accessTokenBearer),
):
    deleted = await BookService.deleteBook(book_uid, session)
    if deleted is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
