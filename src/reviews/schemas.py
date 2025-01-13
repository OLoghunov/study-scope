from typing import Optional
import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class ReviewModel(BaseModel):
    uid: uuid.UUID
    rating: int = Field(lt=6)
    reviewText: str
    userUid: Optional[uuid.UUID]
    bookUid: Optional[uuid.UUID]
    created_at: datetime
    updated_at: datetime


class ReviewCreateModel(BaseModel):
    rating: int = Field(lt=6)
    reviewText: str