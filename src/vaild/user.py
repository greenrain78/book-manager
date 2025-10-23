from src.context import AppContext


def is_book_borrowed(app: AppContext, book_id: int) -> bool:
    return any(borrow.book_id == book_id for borrow in app.borrow.data)