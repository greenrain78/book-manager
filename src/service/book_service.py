from src.context import AppContext
from src.repository.manager import BooksRepository, ISBNRepository, CategoryRepository, BorrowRepository


class BookService:
    def __init__(self, app: AppContext):
        self.app = app
        self.books: BooksRepository = app.books_repo
        self.isbn_repo: ISBNRepository = app.isbn_repo
        self.cat_repo: CategoryRepository = app.cat_repo
        self.borrow_repo: BorrowRepository = app.borrow_repo

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
        # 도서가 대출중인지 확인
        if self.app.borrow_service.is_book_borrowed(book_id=book_id):
            raise RuntimeError("대출중인 도서는 삭제할 수 없습니다.")
        # 도서 삭제
        self.books.delete(book_id)
        # ISBN 도서가 더 이상 Books에 존재하지 않으면 ISBN도 삭제
        remaining_books = self.books.find_by_isbn(book.isbn)
        if not remaining_books:
            self.isbn_repo.delete(book.isbn)
        return None

    def modify_book(self, book_id: str, new_title: str = None, new_author: str = None) -> None:
        book = self.books.find_by_id(book_id)
        if not book:
            raise ValueError("해당 도서를 찾을 수 없습니다.")
        isbn_obj = self.isbn_repo.find(book.isbn)
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

    def search_category(self, cat_id: str):
        return self.cat_repo.find(cat_id)

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
