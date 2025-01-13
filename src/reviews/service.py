from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from fastapi import status

from src.db.models import Review
from src.auth.service import UserService
from src.books.service import BookService
from .schemas import ReviewCreateModel
import logging


bookService = BookService()
userService = UserService()


class ReviewService:
    async def addReviewToBook(
        self,
        userEmail: str,
        bookUid: str,
        reviewData: ReviewCreateModel,
        session: AsyncSession,
    ):
        try:
            book = await bookService.getBook(bookUid=bookUid, session=session)
            user = await userService.getUserByEmail(email=userEmail, session=session)
            reviewDataDict = reviewData.model_dump()
            newReview = Review(**reviewDataDict)

            if not book:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Book not found"
                )
            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            
            newReview.user = user
            newReview.book = book
            session.add(newReview)
            await session.commit()

            return newReview

        except Exception as e:
            logging.exception(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Oops... Something went wrong",
            )
