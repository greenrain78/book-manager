from src.context import AppContext
import re

def is_book_borrowed(app: AppContext, book_id: int) -> bool:
    return any(borrow.book_id == book_id for borrow in app.borrow.data)

def exist_book_title(app: AppContext, title: str) -> bool:
    return any(book.title == title for book in app.books.data)

def exist_book_id(app: AppContext, book_id: int) -> bool:
    return any(book.book_id == book_id for book in app.books.data)

def is_valid_book_title(title: str) -> bool:
    """
    도서 제목 유효성 검사
    :param app:
    :param title:
    :return:
    """
    pattern = r'[A-Za-z0-9]+( [A-Za-z0-9]+)*$'
    if not re.match(pattern, title):
        return False
    return True