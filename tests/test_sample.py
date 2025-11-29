
import unittest
from unittest.mock import patch
from io import StringIO

from src.temp import greet


class TestBasic(unittest.TestCase):
    def test_add(self):
        self.assertEqual(1 + 2, 3)




class TestExample(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 전체 테스트 전에 실행되는 설정 작업
        pass
    @classmethod
    def tearDownClass(cls):
        # 전체 테스트 후에 실행되는 정리 작업
        pass
    def setUp(self):
        # 각 테스트 전에 실행되는 설정 작업
        pass
    def tearDown(self):
        # 각 테스트 후에 실행되는 정리 작업
        pass

    @patch("builtins.input", return_value="철수")
    @patch("sys.stdout", new_callable=StringIO)
    def test_greet(self, mock_stdout, mock_input):
        greet()
        self.assertIn("안녕하세요, 철수님", mock_stdout.getvalue())
