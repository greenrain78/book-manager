import unittest
from io import StringIO
from unittest.mock import patch

from src.prompt.admin import add_book_prompt
from src.repository.entity import ISBN, Book
from src.service.book_service import BookService


class TestAddBookPrompt(unittest.TestCase):

    def setUp(self):
        # Mock BookService
        # 테스트용 순수 Fake 객체 (BookService 상속하지 않음)
        class FakeBookService:
            def __init__(self):
                self.added_books = []  # add_book 호출 내역 저장

            def add_book(self, title: str, author: str) -> None:
                self.added_books.append((title, author))

            # 필요한 경우만 임의로 구현
            def search_isbn_by_title(self, keyword: str):
                return []

            def search_books_by_isbn(self, isbn: str):
                return []

            def search_category(self, cat_id: str):
                return None


        self.book_service = FakeBookService()

    @patch("builtins.input", side_effect=["New Book Title", "Author Name", "Y"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_add_new_book(self, mock_stdout, mock_input):
        add_book_prompt(book_service=self.book_service)
        output = mock_stdout.getvalue()
        self.assertIn("해당 도서를 추가했습니다.", output)

        # 서비스 호출 검증
        self.assertEqual(len(self.book_service.added_books), 1)
        self.assertEqual(self.book_service.added_books[0], ("New Book Title", "Author Name"))

    @patch("builtins.input", side_effect=["Bad  Title", "Good", "Y"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_title_two_spaces_error(self, mock_stdout, mock_input):
        # Bad  Title → 두 칸 공백 → 재입력 요구
        with self.assertRaises(StopIteration):
            # StopIteration 발생: mock input이 고갈될 때 발생 → 정상
            add_book_prompt(self.book_service)

        output = mock_stdout.getvalue()
        self.assertIn("불필요한 공백", output)


    @patch("builtins.input", side_effect=["Java!", "CleanJava", "Y"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_title_special_char_error(self, mock_stdout, mock_input):
        with self.assertRaises(StopIteration):
            add_book_prompt(self.book_service)

        output = mock_stdout.getvalue()
        self.assertIn("불필요한 공백이나 특수문자를 포함", output)

    @patch("builtins.input", side_effect=["", "Java", "Y"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_title_empty_error(self, mock_stdout, mock_input):
        with self.assertRaises(StopIteration):
            add_book_prompt(self.book_service)

        output = mock_stdout.getvalue()
        self.assertIn("도서명은 한글자 이상 입력해야합니다", output)