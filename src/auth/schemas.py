import uuid
from typing import List
from datetime import datetime

from pydantic import BaseModel, Field

from src.books.schemas import BookModel
from src.reviews.schemas import ReviewModel


class UserCreateModel(BaseModel):
    firstName: str = Field(max_length=25)
    lastName: str = Field(max_length=25)
    username: str = Field(max_length=10)
    email: str = Field(max_length=40)
    password: str = Field(min_length=8)


class UserModel(BaseModel):
    uid: uuid.UUID
    username: str
    email: str
    firstName: str
    lastName: str
    isVerified: bool
    passwordHash: str = Field(exclude=True)
    created_at: datetime
    updated_at: datetime
    
    
class UserBooksModel(UserModel):
    books: List[BookModel]
    reviews: List[ReviewModel]


class UserLoginModel(BaseModel):
    email: str = Field(max_length=40)
    password: str = Field(min_length=8)


class EmailModel(BaseModel):
    addresses: List[str]