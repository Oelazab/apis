from fastapi import FastAPI, HTTPException, status
from typing import List
from models import Book, BookCreate, BookUpdate

app = FastAPI(
    title="Book Library API",
    description="A simple RESTful API to manage a book collection",
    version="1.0.0",
)

# In-memory database (list of books)
books_db = []
current_id = 1


# Helper to find a book by id
def find_book(book_id: int):
    for book in books_db:
        if book["id"] == book_id:
            return book
    return None


# ----------------------------------------------------------------------------- CRUD Endpoints
@app.get("/books", response_model=List[Book], status_code=status.HTTP_200_OK)
async def get_all_books():
    """Retrieve all books in the library."""
    return books_db


@app.get("/books/{book_id}", response_model=Book)
async def get_book(book_id: int):
    """Retrieve a single book by its ID."""
    book = find_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.post("/books", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_book(new_book: BookCreate):
    """Add a new book to the library."""
    global current_id
    book_dict = new_book.dict()
    book_dict["id"] = current_id
    books_db.append(book_dict)
    current_id += 1
    return book_dict


@app.put("/books/{book_id}", response_model=Book)
async def update_book(book_id: int, updated_data: BookUpdate):
    """Fully or partially update an existing book."""
    book = find_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    # Update only fields that are provided
    update_dict = updated_data.dict(exclude_unset=True)
    for key, value in update_dict.items():
        book[key] = value
    return book


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    """Remove a book from the library."""
    book = find_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    books_db.remove(book)
    return  # No content
