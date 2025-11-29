from src.repository.manager import BooksRepository, ISBNRepository, CategoryRepository


class BookService:
    def __init__(self, repository: BooksRepository, isbn_repo: ISBNRepository, cat_repo: CategoryRepository):
        self.books: BooksRepository = repository
        self.isbn_repo: ISBNRepository = isbn_repo
        self.cat_repo: CategoryRepository = cat_repo

    def search_book_by_title(self, keyword) -> list:
        # 키워드로 isbn_repo에서 도서 검색
        # 다시 books_repo에서 book_id로 도서 정보 가져오기
        matched_isbns = self.isbn_repo.find_by_title(keyword)
        matched_books = []
        for isbn_obj in matched_isbns:
            matched_books.extend(self.books.find_by_isbn(isbn_obj.isbn))
        return matched_books
