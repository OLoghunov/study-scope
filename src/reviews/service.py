from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from fastapi import status
from sqlmodel import select

from src.db.models import Review
from src.auth.service import UserService
from src.books.service import BookService
from .schemas import ReviewCreateModel
import logging


bookService = BookService()
userService = UserService()


class ReviewService:
    async def getAllUserReviews(self, userUid: str, session: AsyncSession):
        try:
            statement = select(Review).where(Review.userUid == userUid)
            result = await session.exec(statement)
        except Exception as e:
            logging.exception(e)
            return None

        return result.all()
    
    async def getReview(self, userUid: str, reviewUid: str, session: AsyncSession):
        try:
            statement = select(Review).where(Review.uid == reviewUid and Review.userUid == userUid)
            result = await session.exec(statement)
        except Exception as e:
            logging.exception(e)
            return None

        return result.first()
    
    
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
            
            
    async def deleteReviewByUid(
        self,
        userEmail: str,
        reviewUid: str,
        session: AsyncSession,
    ):
        try:
            user = await userService.getUserByEmail(email=userEmail, session=session)
            reviewToDelete = await self.getReview(user.uid, reviewUid, session)
            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
                
            if not reviewToDelete:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Review not found"
                )
            
            await session.delete(reviewToDelete)
            await session.commit()

            return {}

        except Exception as e:
            logging.exception(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Oops... Something went wrong",
            )
