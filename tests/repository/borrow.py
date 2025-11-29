import unittest
import tempfile
import os

from src.repository.entity import Borrow
from src.repository.manager import BorrowRepository


class TestBorrowRepository(unittest.TestCase):

    def setUp(self):
        """
        테스트용 임시 파일 생성
        파일 형식: book_id | user_id | borrow_date | due_date
        """
        self.tmp = tempfile.NamedTemporaryFile(delete=False, mode="w+")
        self.path = self.tmp.name

        # 영어 테스트 데이터
        self.tmp.write("B001|U001|2024-01-01|2024-01-15\n")
        self.tmp.write("B002|U002|2024-02-01|2024-02-15\n")
        self.tmp.close()

    def tearDown(self):
        """
        테스트 종료 후 임시 파일 삭제
        """
        os.unlink(self.path)

    def test_load_all(self):
        """
        파일 로드 테스트
        """
        repo = BorrowRepository(self.path)

        self.assertEqual(len(repo.data), 2)
        self.assertEqual(repo.data[0].book_id, "B001")
        self.assertEqual(repo.data[0].user_id, "U001")
        self.assertEqual(repo.data[0].borrow_date, "2024-01-01")
        self.assertEqual(repo.data[0].due_date, "2024-01-15")

    def test_insert(self):
        """
        대출 정보 추가 후 파일 저장 여부 검증
        """
        repo = BorrowRepository(self.path)

        new_borrow = Borrow(
            book_id="B003",
            user_id="U003",
            borrow_date="2024-03-01",
            due_date="2024-03-15"
        )
        repo.insert(new_borrow)

        self.assertEqual(len(repo.data), 3)
        self.assertEqual(repo.data[-1].user_id, "U003")

        repo2 = BorrowRepository(self.path)
        self.assertEqual(len(repo2.data), 3)
        self.assertEqual(repo2.data[-1].book_id, "B003")

    def test_delete(self):
        """
        특정 book_id 대출 기록 삭제 테스트
        """
        repo = BorrowRepository(self.path)

        repo.delete("B001")

        self.assertEqual(len(repo.data), 1)
        self.assertEqual(repo.data[0].book_id, "B002")

        repo2 = BorrowRepository(self.path)
        self.assertEqual(len(repo2.data), 1)

    def test_invalid_format_raises(self):
        """
        필드 개수 부족한 잘못된 데이터 라인은 오류 발생해야 함
        """
        invalid_tmp = tempfile.NamedTemporaryFile(delete=False, mode="w+")
        path = invalid_tmp.name

        # expected_fields=4 → "|"는 3개여야 한다
        invalid_tmp.write("B001|U001|only_three_fields\n")  # 파이프 개수=2 → 오류
        invalid_tmp.close()

        with self.assertRaises(RuntimeError):
            BorrowRepository(path)

        os.unlink(path)

    def test_blank_line_raises(self):
        """
        빈 줄이 존재하면 오류 발생해야 함
        """
        invalid_tmp = tempfile.NamedTemporaryFile(delete=False, mode="w+")
        path = invalid_tmp.name

        invalid_tmp.write("\n")
        invalid_tmp.close()

        with self.assertRaises(RuntimeError):
            BorrowRepository(path)

        os.unlink(path)

