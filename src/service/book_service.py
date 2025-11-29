from src.repository.manager import BooksRepository


class BookService:
    def __init__(self, repository: BooksRepository):
        self.books: BooksRepository = repository

    def search_book_by_title(self, keyword):
        keyword_lower = keyword.lower()
        return [book for book in self.books.data if keyword_lower in book.title.lower()]


    def _exist_book_title(self, title: str) -> bool:
        return any(title.lower() in book.title.lower() for book in self.books.data)
