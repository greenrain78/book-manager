from src.context import AppContext
from src.repository.entity import ISBN, Category, Book
from src.repository.manager import BooksRepository, ISBNRepository, CategoryRepository, BorrowRepository
from src.service import borrow_service
from src.service.borrow_service import BorrowService


class BookService:
    def __init__(self, app: AppContext, navi = None):
        self.app = app
        self.books: BooksRepository = app.books_repo
        self.isbn_repo: ISBNRepository = app.isbn_repo
        self.cat_repo: CategoryRepository = app.cat_repo
        self.borrow_service: BorrowService = borrow_service.BorrowService(app)

    # 도서 추가
    def add_book(self, title: str, author: str) -> None:
        # ISBN 추가
        isbn_obj = self.isbn_repo.find_by_title_and_author(title, author)
        if not isbn_obj:
            isbn_obj = self.isbn_repo.insert(title=title, author=author, cat_id="CAT00")
        # Books 추가
        self.books.insert(isbn=isbn_obj.isbn)
        return None

    def delete_book(self, book_id: str) -> None:
        book = self.books.find_by_id(book_id)
        if not book:
            raise ValueError("해당 도서를 찾을 수 없습니다.")
        # 도서 삭제
        self.books.delete(book_id)
        # ISBN 도서가 더 이상 Books에 존재하지 않으면 ISBN도 삭제
        remaining_books = self.books.find_by_isbn(book.isbn)
        if not remaining_books:
            self.isbn_repo.delete(book.isbn)
        return None

    def modify_book(self, isbn: str, new_title: str = None, new_author: str = None) -> None:
        isbn_obj = self.isbn_repo.find(isbn)
        if not isbn_obj:
            raise ValueError("해당 ISBN 도서를 찾을 수 없습니다.")
        # ISBN 정보 수정
        self.isbn_repo.modify(
            isbn=isbn_obj.isbn,
            new_title=new_title,
            new_author=new_author
        )
        return None

    def search_isbn_by_title(self, keyword: str) -> list:
        return self.isbn_repo.find_by_title(keyword)

    def search_book_by_id(self, book_id: str):
        return self.books.find_by_id(book_id)

    def search_books_by_isbn(self, isbn: str) -> list:
        return self.books.find_by_isbn(isbn)

    def read_books_by_isbn(self, isbn: ISBN) -> list[dict]:
        """
        보기 좋게 도서 정보 반환
        """
        books = self.books.find_by_isbn(isbn=isbn.isbn)
        categorys = [self.cat_repo.find(cat_id) for cat_id in isbn.cat_id.split(';')]

        result = []
        for book in books:
            result.append({
                "book_id": book.book_id,
                "title": isbn.title,
                "author": isbn.author,
                "category": ";".join([cat.cat_name for cat in categorys if cat]) if categorys else "uncategorized",
                "status": "대출중" if self.borrow_service.is_book_borrowed(book.book_id) else "대여가능"
            })
        return result
    def search_isbn(self, isbn: str) -> ISBN | None:
        return self.isbn_repo.find(isbn)

    def search_category(self, cat_id: str) -> Category | None:
        return self.cat_repo.find(cat_id)

    def search_category_by_name(self, keyword: str) -> list:
        return self.cat_repo.find_by_name(keyword)

    def search_book_by_title(self, keyword) -> list:
        if not keyword:
            return []
        # 키워드로 isbn_repo에서 도서 검색
        # 다시 books_repo에서 book_id로 도서 정보 가져오기
        matched_isbns = self.isbn_repo.find_by_title(keyword)
        matched_books = []
        for isbn_obj in matched_isbns:
            matched_books.extend(self.books.find_by_isbn(isbn_obj.isbn))
        return matched_books
