
import unittest
from unittest.mock import patch
from io import StringIO

from src.temp import greet





class TestUserPrompt(unittest.TestCase):

    @patch("builtins.input", return_value="1")
    @patch("sys.stdout", new_callable=StringIO)
    def test_book_search_prompt(self, mock_stdout, mock_input):
        greet()
        self.assertIn("안녕하세요, 철수님", mock_stdout.getvalue())
