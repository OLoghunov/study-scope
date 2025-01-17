from typing import List

from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.models import User
from src.db.main import getSession
from src.auth.dependencies import getCurrentUser
from .schemas import ReviewCreateModel, ReviewShortModel
from .service import ReviewService


reviewRouter = APIRouter()
reviewService = ReviewService()


@reviewRouter.post("/book/{bookUid}")
async def addReviewToBook(
    bookUid: str,
    reviewData: ReviewCreateModel,
    currentUser: User = Depends(getCurrentUser),
    session: AsyncSession = Depends(getSession),
):
    newReview = await reviewService.addReviewToBook(
        userEmail=currentUser.email,
        reviewData=reviewData,
        bookUid=bookUid,
        session=session,
    )

    return newReview


@reviewRouter.delete("/book/{reviewUid}")
async def deleteReviewByUid(
    reviewUid: str,
    currentUser: User = Depends(getCurrentUser),
    session: AsyncSession = Depends(getSession),
):
    await reviewService.deleteReviewByUid(currentUser.email, reviewUid, session)

    return {}


@reviewRouter.get("/my", response_model=List[ReviewShortModel])
async def getAllUserReviews(
    user: User = Depends(getCurrentUser), session=Depends(getSession)
):
    reviews = await reviewService.getAllUserReviews(user.uid, session)
    return reviews
