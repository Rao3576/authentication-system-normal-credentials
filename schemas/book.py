# schemas/book.py
from pydantic import BaseModel

class AuthorBase(BaseModel):
    name: str

class AuthorCreate(AuthorBase):
    pass

class AuthorOut(AuthorBase):
    id: int
    class Config:
        orm_mode = True

class BookBase(BaseModel):
    title: str
    author_id: int

class BookCreate(BookBase):
    pass

class BookOut(BookBase):
    id: int
    author: AuthorOut
    class Config:
        orm_mode = True

