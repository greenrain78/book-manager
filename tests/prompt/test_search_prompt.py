
import unittest
from io import StringIO
from unittest.mock import patch

from src.prompt.search import search_by_book_prompt
from src.repository.entity import ISBN, Book
from src.service.book_service import BookService


class TestSearchByBookPrompt(unittest.TestCase):

    def setUp(self):
        class FakeBookService(BookService):
            def __init__(self):
                pass # 부모 생성자 호출 안 함

            def search_isbn_by_title(self, keyword: str):
                if keyword == "Existing Book":
                    return [
                        ISBN(isbn="ISBN01", title="Existing Book", author="Author A", cat_id="CAT01"),
                        ISBN(isbn="ISBN02", title="Existing Book", author="Author B", cat_id="CAT02"),
                    ]
                else:
                    return []

            def search_books_by_isbn(self, isbn: str):
                if isbn == "ISBN01":
                    return [Book(book_id="001", isbn="ISBN01"), Book(book_id="002", isbn="ISBN02")]
                elif isbn == "ISBN02":
                    return [Book(book_id="003", isbn="ISBN02")]
                else:
                    return []

            def search_category(self, cat_id: str):
                if cat_id == "CAT01":
                    class Category:
                        name = "Fiction"
                    return Category()
                elif cat_id == "CAT02":
                    class Category:
                        name = "Non-Fiction"
                    return Category()
                return None

            def is_book_borrowed(self, book_id: str):
                if book_id == "001":
                    return False
                elif book_id == "002":
                    return True
                elif book_id == "003":
                    return False
                return None

        self.book_service = FakeBookService()


    @patch("builtins.input", return_value="Existing Book")
    @patch("sys.stdout", new_callable=StringIO)
    def test_search_existing_book(self, mock_stdout, mock_input):
        search_by_book_prompt(service=self.book_service)
        output = mock_stdout.getvalue()
        self.assertIn("대여가능 | 001", output)
        self.assertIn("대출중 | 002", output)

    @patch("builtins.input", return_value="Nonexistent Book")
    @patch("sys.stdout", new_callable=StringIO)
    def test_search_nonexistent_book(self, mock_stdout, mock_input):
        search_by_book_prompt(service=self.book_service)
        output = mock_stdout.getvalue()
        self.assertIn("목록에 존재하지 않는 도서입니다.!! 올바른 제목을 입력하세요.", output)

    # ────────────────────────────────────────────────
    # 공백 오류
    # ────────────────────────────────────────────────
    @patch("builtins.input", return_value=" Computer Science")
    @patch("sys.stdout", new_callable=StringIO)
    def test_invalid_input_leading_space(self, mock_stdout, mock_input):
        search_by_book_prompt(service=self.book_service)
        self.assertIn("올바른 제목을 입력하세요", mock_stdout.getvalue())

    @patch("builtins.input", return_value="Computer Science ")
    @patch("sys.stdout", new_callable=StringIO)
    def test_invalid_input_trailing_space(self, mock_stdout, mock_input):
        search_by_book_prompt(service=self.book_service)
        self.assertIn("올바른 제목을 입력하세요", mock_stdout.getvalue())

    @patch("builtins.input", return_value=" Computer Science ")
    @patch("sys.stdout", new_callable=StringIO)
    def test_invalid_input_both_side_space(self, mock_stdout, mock_input):
        search_by_book_prompt(service=self.book_service)
        self.assertIn("올바른 제목을 입력하세요", mock_stdout.getvalue())

    @patch("builtins.input", side_effect=["Computer  Science", "Existing Book"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_invalid_input_double_middle_space(self, mock_stdout, mock_input):
        search_by_book_prompt(service=self.book_service)
        self.assertIn("올바른 제목을 입력하세요", mock_stdout.getvalue())
        output = mock_stdout.getvalue()
        self.assertIn("대여가능 | 001", output)
        self.assertIn("대출중 | 002", output)


    # ────────────────────────────────────────────────
    # 특수문자 오류
    # ────────────────────────────────────────────────
    @patch("builtins.input", side_effect=["Computer!", "Existing Book"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_invalid_input_special_char_end(self, mock_stdout, mock_input):
        search_by_book_prompt(service=self.book_service)
        self.assertIn("올바른 제목을 입력하세요", mock_stdout.getvalue())
        output = mock_stdout.getvalue()
        self.assertIn("대여가능 | 001", output)
        self.assertIn("대출중 | 002", output)

    @patch("builtins.input", side_effect=["!", "Existing Book"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_invalid_input_special_char_only(self, mock_stdout, mock_input):
        search_by_book_prompt(service=self.book_service)
        self.assertIn("올바른 제목을 입력하세요", mock_stdout.getvalue())
        output = mock_stdout.getvalue()
        self.assertIn("대여가능 | 001", output)
        self.assertIn("대출중 | 002", output)


    # ────────────────────────────────────────────────
    # 형식 오류
    # ────────────────────────────────────────────────
    @patch("builtins.input", side_effect=["-1", "Existing Book"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_invalid_input_negative_number(self, mock_stdout, mock_input):
        search_by_book_prompt(service=self.book_service)
        self.assertIn("올바른 제목을 입력하세요", mock_stdout.getvalue())
        output = mock_stdout.getvalue()
        self.assertIn("대여가능 | 001", output)
        self.assertIn("대출중 | 002", output)


    @patch("builtins.input", side_effect=["1.0", "Existing Book"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_invalid_input_float_number(self, mock_stdout, mock_input):
        search_by_book_prompt(service=self.book_service)
        self.assertIn("올바른 제목을 입력하세요", mock_stdout.getvalue())
        output = mock_stdout.getvalue()
        self.assertIn("대여가능 | 001", output)
        self.assertIn("대출중 | 002", output)


    # ────────────────────────────────────────────────
    # 빈 문자열 / 탭 포함
    # ────────────────────────────────────────────────
    @patch("builtins.input", side_effect=["", "Existing Book"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_invalid_input_empty_string(self, mock_stdout, mock_input):
        search_by_book_prompt(service=self.book_service)
        self.assertIn("올바른 제목을 입력하세요", mock_stdout.getvalue())
        output = mock_stdout.getvalue()
        self.assertIn("대여가능 | 001", output)
        self.assertIn("대출중 | 002", output)

    @patch("builtins.input", return_value="\tComputer")
    @patch("sys.stdout", new_callable=StringIO)
    def test_invalid_input_tab_leading(self, mock_stdout, mock_input):
        search_by_book_prompt(service=self.book_service)
        self.assertIn("올바른 제목을 입력하세요", mock_stdout.getvalue())


    @patch("builtins.input", side_effect=["Computer\tScience", "Existing Book"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_invalid_input_tab_middle(self, mock_stdout, mock_input):
        search_by_book_prompt(service=self.book_service)
        self.assertIn("올바른 제목을 입력하세요", mock_stdout.getvalue())
        output = mock_stdout.getvalue()
        self.assertIn("대여가능 | 001", output)
        self.assertIn("대출중 | 002", output)