import tempfile
import unittest
import os

from src.repository.manager import BooksRepository, ISBNRepository, CategoryRepository
from src.service.cat_service import CategoryService


class TestCategorySearchIntegration(unittest.TestCase):

    def setUp(self):
        self.books = tempfile.NamedTemporaryFile(delete=False, mode="w+", encoding="utf-8")
        self.isbns = tempfile.NamedTemporaryFile(delete=False, mode="w+", encoding="utf-8")
        self.cats = tempfile.NamedTemporaryFile(delete=False, mode="w+", encoding="utf-8")

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

        self.book_repo = BooksRepository(self.books.name)
        self.isbn_repo = ISBNRepository(self.isbns.name)
        self.cat_repo = CategoryRepository(self.cats.name)

        class FakeAppContext:
            def __init__(self, books_repo, isbn_repo, cat_repo):
                self.books_repo = books_repo
                self.isbn_repo = isbn_repo
                self.cat_repo = cat_repo
        app = FakeAppContext(
            books_repo=self.book_repo,
            isbn_repo=self.isbn_repo,
            cat_repo=self.cat_repo
        )
        self.service = CategoryService(app=app)

    def tearDown(self):
        os.unlink(self.books.name)
        os.unlink(self.isbns.name)
        os.unlink(self.cats.name)

    def test_category_and(self):
        result = self.service.search_by_category("science&space")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].isbn, "ISBN01")
        self.assertEqual(result[0].cat_id, "CAT01;CAT02")


    def test_category_not(self):
        result = self.service.search_by_category("!science")
        # science 포함하는 ISBN01 제외 → ISBN02만 남음
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].isbn, "ISBN02")
        self.assertEqual(result[0].cat_id, "CAT03")

    def test_category_or(self):
        result = self.service.search_by_category("science|math")
        ids = sorted([b.isbn for b in result])
        self.assertEqual(ids, ["ISBN01", "ISBN02"])
