import unittest
import tempfile
import os

from src.repository.entity import BorrowHistory
from src.repository.manager import BorrowHistoryRepository


class TestBorrowHistoryRepository(unittest.TestCase):

    def setUp(self):
        """
        테스트용 임시 파일 생성 (영문 데이터)
        파일 형식: book_id | user_id | borrow_date | due_date | return_date
        """
        self.tmp = tempfile.NamedTemporaryFile(delete=False, mode="w+")
        self.path = self.tmp.name

        self.tmp.write("B001|U001|2024-01-01|2024-01-15|2024-01-10\n")
        self.tmp.write("B002|U002|2024-02-01|2024-02-15|2024-02-12\n")
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
        repo = BorrowHistoryRepository(self.path)

        self.assertEqual(len(repo.data), 2)
        self.assertEqual(repo.data[0].book_id, "B001")
        self.assertEqual(repo.data[0].user_id, "U001")
        self.assertEqual(repo.data[0].borrow_date, "2024-01-01")
        self.assertEqual(repo.data[0].due_date, "2024-01-15")
        self.assertEqual(repo.data[0].return_date, "2024-01-10")

    def test_insert(self):
        """
        대출 기록 히스토리 추가 후 파일 저장 여부 확인
        """
        repo = BorrowHistoryRepository(self.path)

        new_entry = BorrowHistory(
            book_id="B003",
            user_id="U003",
            borrow_date="2024-03-01",
            due_date="2024-03-15",
            return_date="2024-03-12"
        )
        repo.insert(new_entry)

        self.assertEqual(len(repo.data), 3)
        self.assertEqual(repo.data[-1].user_id, "U003")

        repo2 = BorrowHistoryRepository(self.path)
        self.assertEqual(len(repo2.data), 3)
        self.assertEqual(repo2.data[-1].return_date, "2024-03-12")

    def test_invalid_format_raises(self):
        """
        필드 개수가 부족한 경우 RuntimeError 발생 여부 확인
        """
        invalid_tmp = tempfile.NamedTemporaryFile(delete=False, mode="w+")
        path = invalid_tmp.name

        # expected_fields=5 → 파이프(|) 4개여야 하나 실제로는 3개
        invalid_tmp.write("B001|U001|2024-01-01|2024-01-15\n")
        invalid_tmp.close()

        with self.assertRaises(RuntimeError):
            BorrowHistoryRepository(path)

        os.unlink(path)

    def test_blank_line_raises(self):
        """
        빈 줄이 있으면 오류 발생해야 함
        """
        invalid_tmp = tempfile.NamedTemporaryFile(delete=False, mode="w+")
        path = invalid_tmp.name

        invalid_tmp.write("\n")
        invalid_tmp.close()

        with self.assertRaises(RuntimeError):
            BorrowHistoryRepository(path)

        os.unlink(path)
