from src.repository.manager import BooksRepository, ISBNRepository, CategoryRepository, BorrowRepository


class BookService:
    def __init__(
            self,
            books_repo: BooksRepository,
            isbn_repo: ISBNRepository,
            cat_repo: CategoryRepository,
            borrow_repo: BorrowRepository
    ):
        self.books: BooksRepository = books_repo
        self.isbn_repo: ISBNRepository = isbn_repo
        self.cat_repo: CategoryRepository = cat_repo
        self.borrow_repo: BorrowRepository = borrow_repo

    def search_isbn_by_title(self, keyword: str) -> list:
        return self.isbn_repo.find_by_title(keyword)

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

    # 대출중인지 확인
    def is_book_borrowed(self, book_id: str) -> bool:
        for borrow in self.borrow_repo.data:
            if borrow.book_id == book_id:
                return True
        return False