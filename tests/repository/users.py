import unittest
import tempfile
import os

from src.repository.entity import User
from src.repository.manager import UsersRepository


class TestUsersRepository(unittest.TestCase):

    def setUp(self):
        """
        테스트용 임시 파일 생성
        """
        self.tmp = tempfile.NamedTemporaryFile(delete=False, mode="w+")
        self.path = self.tmp.name

        # 파일 형식: user_id | pw | email
        self.tmp.write("001|pass123|john@example.com|2025-01-08\n")
        self.tmp.write("002|hello2024|alice@example.com|2025-02-10\n")
        self.tmp.close()

    def tearDown(self):
        """
        테스트 종료 후 임시 파일 삭제
        """
        os.unlink(self.path)

    def test_load_all(self):
        """
        파일 로드가 정상적으로 이루어지는지 확인
        """
        repo = UsersRepository(self.path)

        self.assertEqual(len(repo.data), 2)
        self.assertEqual(repo.data[0].user_id, "001")
        self.assertEqual(repo.data[0].pw, "pass123")
        self.assertEqual(repo.data[0].email, "john@example.com")
        self.assertEqual(repo.data[0].penaltyDate, "2025-01-08")

    def test_insert(self):
        """
        새로운 사용자 추가 후 파일 저장 여부 확인
        """
        repo = UsersRepository(self.path)

        new_user = User(user_id="003", pw="mypw", email="charlie@example.com", penaltyDate="2025-03-15")
        repo.insert(new_user)

        # 메모리 데이터 확인
        self.assertEqual(len(repo.data), 3)
        self.assertEqual(repo.data[-1].email, "charlie@example.com")

        # 파일 재로드하여 확인
        repo2 = UsersRepository(self.path)
        self.assertEqual(len(repo2.data), 3)
        self.assertEqual(repo2.data[-1].pw, "mypw")

    def test_invalid_file_format_raises(self):
        """
        필드 개수가 부족한 잘못된 데이터 라인은 오류가 발생해야 함
        """
        invalid_tmp = tempfile.NamedTemporaryFile(delete=False, mode="w+")
        path = invalid_tmp.name

        # expected_fields=4인데 필드가 2개뿐
        invalid_tmp.write("001|only_pw\n")
        invalid_tmp.close()

        with self.assertRaises(RuntimeError):
            UsersRepository(path)

        os.unlink(path)

    def test_blank_line_raises(self):
        """
        빈 줄이 존재하면 오류가 발생해야 함
        """
        invalid_tmp = tempfile.NamedTemporaryFile(delete=False, mode="w+")
        path = invalid_tmp.name

        invalid_tmp.write("\n")
        invalid_tmp.close()

        with self.assertRaises(RuntimeError):
            UsersRepository(path)

        os.unlink(path)


