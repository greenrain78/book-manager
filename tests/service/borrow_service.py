import tempfile
import unittest
import os

from src.repository.manager import BooksRepository, ISBNRepository, CategoryRepository, UsersRepository, \
    BorrowRepository, BorrowHistoryRepository
from src.service.book_service import BookService
from src.service.borrow_service import BorrowService
from src.service.cat_service import CategoryService


class TestBookServiceIntegration2(unittest.TestCase):

    def setUp(self):
        self.books = tempfile.NamedTemporaryFile(delete=False, mode="w+", encoding="utf-8")
        self.isbns = tempfile.NamedTemporaryFile(delete=False, mode="w+", encoding="utf-8")
        self.cats = tempfile.NamedTemporaryFile(delete=False, mode="w+", encoding="utf-8")
        self.users = tempfile.NamedTemporaryFile(delete=False, mode="w+", encoding="utf-8")
        self.borrows = tempfile.NamedTemporaryFile(delete=False, mode="w+", encoding="utf-8")
        self.borrow_history = tempfile.NamedTemporaryFile(delete=False, mode="w+", encoding="utf-8")


        # categories
        self.cats.write("CAT01|science\n")
        self.cats.write("CAT02|space\n")
        self.cats.write("CAT03|math\n")
        self.cats.close()

        # isbn
        self.isbns.write("ISBN01|Bigbang1|Jensen|CAT01;CAT02\n")
        self.isbns.write("ISBN02|MathBook|John|CAT03\n")
        self.isbns.close()

        # books
        self.books.write("003|ISBN01\n")
        self.books.write("004|ISBN02\n")
        self.books.close()

        # users
        self.users.write("korea123|ab1234!@|abc@naver.com|2025-01-08\n")
        self.users.write("english456|cd5678!@|kkk@gmail.com|\n")
        self.users.close()

        # borrows
        self.borrows.write("003|korea123|2024-05-01|2024-05-15\n")
        self.borrows.close()

        # borrow history
        self.borrow_history.write("003|korea123|2024-01-01|2024-01-15|2024-01-10\n")
        self.borrow_history.close()

        self.book_repo = BooksRepository(self.books.name)
        self.isbn_repo = ISBNRepository(self.isbns.name)
        self.cat_repo = CategoryRepository(self.cats.name)
        self.users_repo = UsersRepository(self.users.name)
        self.borrow_repo = BorrowRepository(self.borrows.name)
        self.borrow_history_repo = BorrowHistoryRepository(self.borrow_history.name)

        class FakeAppContext:
            current_user = None
            def __init__(self, books_repo, isbn_repo, cat_repo, users_repo, borrow_repo, borrow_history_repo):
                self.books_repo = books_repo
                self.isbn_repo = isbn_repo
                self.cat_repo = cat_repo
                self.users_repo = users_repo
                self.borrow_repo = borrow_repo
                self.borrow_history_repo = borrow_history_repo

        self.app = FakeAppContext(
            books_repo=self.book_repo,
            isbn_repo=self.isbn_repo,
            cat_repo=self.cat_repo,
            users_repo=self.users_repo,
            borrow_repo=self.borrow_repo,
            borrow_history_repo=self.borrow_history_repo
        )
        self.service = BorrowService(app=self.app)

    def tearDown(self):
        os.unlink(self.books.name)
        os.unlink(self.isbns.name)
        os.unlink(self.cats.name)


    # 연체일 조회
    def test_get_user_penalty_date(self):
        self.app.current_user = self.users_repo.find_by_id("korea123")
        penalty_date = self.service.get_user_penalty_date()
        self.assertIsNotNone(penalty_date)
        self.assertEqual(penalty_date.strftime("%Y-%m-%d"), "2025-01-08")
