import os
import tempfile
import unittest

from src.repository.manager import BooksRepository, ISBNRepository, CategoryRepository
from src.service.book_service import BookService

"""
개발의 편리성과 테스트의 용이함을 위해 service는 repository 합쳐서 통합 테스트만 진행합니다.
"""

class TestBookServiceIntegration(unittest.TestCase):

    def setUp(self):
        # 임시 파일 생성
        self.books = tempfile.NamedTemporaryFile(delete=False, mode="w+", encoding="utf-8")
        self.path1 = self.books.name
        self.isbn = tempfile.NamedTemporaryFile(delete=False, mode="w+", encoding="utf-8")
        self.path2 = self.isbn.name
        self.categories = tempfile.NamedTemporaryFile(delete=False, mode="w+", encoding="utf-8")
        self.path3 = self.categories.name

        # 테스트용 초기 데이터 작성
        # expected_fields = 3 → book_id | title | author
        # books.txt에    007|ISBN07
        # ISBN.txt에 	ISBN07|Computer Science|Elon␣musk|CAT01
        # categories.txt에	 CAT01|computer

        self.books.write("007|ISBN07\n")
        self.books.close()
        self.isbn.write("ISBN07|Computer Science|Elon musk|CAT01\n")
        self.isbn.close()
        self.categories.write("CAT01|computer\n")
        self.categories.close()

        # 통합 테스트: 실제 Repository + 실제 Service
        self.book_repo = BooksRepository(self.path1)
        self.isbn_repo = ISBNRepository(self.path2)
        self.cat_repo = CategoryRepository(self.path3)

        self.service = BookService(self.book_repo, self.isbn_repo, self.cat_repo)


    def tearDown(self):
        # 테스트 파일 삭제
        os.unlink(self.path1)
        os.unlink(self.path2)
        os.unlink(self.path3)

    def test_search_book_by_title_exact_match(self):
        """
        정상 케이스: 정확한 도서명 검색
        Document Case:
        - 입력: "Computer Science"
        - 결과: 책 상태, book_id, title, author, category 매칭
        """
        # when
        result = self.service.search_book_by_title("Computer Science")

        # then
        self.assertEqual(len(result), 1)
        book = result[0]
        self.assertEqual(book.book_id, "007")
        self.assertEqual(book.isbn, "ISBN07")

        # ISBN 매핑도 검증
        isbn = self.isbn_repo.find_by_isbn("ISBN07")
        self.assertEqual(isbn.title, "Computer Science")
        self.assertEqual(isbn.author, "Elon musk")
        self.assertEqual(isbn.cat_id, "CAT01")

    def test_search_book_by_title_partial_match(self):
        """
        부분 일치 검색
        Document Case:
        - 입력: "Science", "com", "computer"
        """
        # when
        result1 = self.service.search_book_by_title("Science")
        result2 = self.service.search_book_by_title("com")
        result3 = self.service.search_book_by_title("computer")

        # then
        self.assertEqual(len(result1), 1)
        self.assertEqual(result1[0].book_id, "007")

        self.assertEqual(len(result2), 1)
        self.assertEqual(result2[0].book_id, "007")

        self.assertEqual(len(result3), 1)
        self.assertEqual(result3[0].book_id, "007")

    def test_search_book_by_title_case_insensitive_match(self):
        """
        대소문자 무시 검색
        Document Case:
        - 입력: "computer science", "COMPUTER SCIENCE"
        """
        result1 = self.service.search_book_by_title("computer science")
        result2 = self.service.search_book_by_title("COMPUTER SCIENCE")

        self.assertEqual(len(result1), 1)
        self.assertEqual(len(result2), 1)

        self.assertEqual(result1[0].book_id, "007")
        self.assertEqual(result2[0].book_id, "007")


    def test_search_book_by_title_not_found(self):
        """
        존재하지 않는 도서 검색
        Document Case:
        - 입력: "Computer Graphics"
        - 출력: []
        """
        result = self.service.search_book_by_title("Computer Graphics")
        self.assertEqual(result, [])


    def test_search_book_by_title_special_character(self):
        """
        특수문자 포함 검색 → 일치하는 title이 없으므로 결과 없음
        문서 기준: 입력 단계에서 막아야 하지만 서비스는 단순 검색 기능
        """
        result = self.service.search_book_by_title("Science!")

        self.assertEqual(result, [])