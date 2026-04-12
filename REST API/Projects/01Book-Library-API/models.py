from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    author: str = Field(..., min_length=1, max_length=100)
    published_year: int = Field(..., ge=1450, le=datetime.now().year)
    genre: Optional[str] = None


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    author: Optional[str] = Field(None, min_length=1, max_length=100)
    published_year: Optional[int] = Field(None, ge=1450, le=datetime.now().year)
    genre: Optional[str] = None


class Book(BookBase):
    id: int
