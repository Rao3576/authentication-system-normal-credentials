# routes/book.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.book import Author, Book
from schemas.book import AuthorCreate, AuthorOut, BookCreate, BookOut
from utils.jwt import get_current_user  # ✅ already exists

router = APIRouter(prefix="/books", tags=["Books & Authors"])

# Create Author
@router.post("/authors", response_model=AuthorOut)
def create_author(author: AuthorCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    new_author = Author(name=author.name)
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author

# Get Authors
@router.get("/authors", response_model=list[AuthorOut])
def get_authors(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return db.query(Author).all()

# Create Book
@router.post("/", response_model=BookOut)
def create_book(book: BookCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    author = db.query(Author).filter(Author.id == book.author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    new_book = Book(title=book.title, author_id=book.author_id)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

# Get Books
@router.get("/", response_model=list[BookOut])
def get_books(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return db.query(Book).all()

# Update Book (Admin only)
@router.put("/{book_id}", response_model=BookOut)
def update_book(book_id: int, book: BookCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    db_book.title = book.title
    db_book.author_id = book.author_id
    db.commit()
    db.refresh(db_book)
    return db_book

# Delete Book (Admin only)
@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    db.delete(db_book)
    db.commit()
    return {"detail": "Book deleted successfully"}


