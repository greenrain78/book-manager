from datetime import datetime

from src.prompt.user import borrow_prompt, return_prompt
from src.repository.entity import User
from src.service.book_service import BookService
from src.service.borrow_service import BorrowService
from tests.common import PromptTestBase


class BorrowPromptTest(PromptTestBase):
    ENABLE_FILE_PRINT = True   # 확인용 출력 ON/OFF
    ENABLE_FILE_CLEANUP = True # 테스트 파일 삭제 ON/OFF

    # borrow_prompt 실행 + 출력 캡처
    def execute_borrow_prompt(self, book_service, borrow_service, input_values):
        return self.execute_prompt(
            input_values, borrow_prompt, 
            book_service=book_service, borrow_service=borrow_service
        )


    # ---------------------------------------------------
    # Test Scenarios
    # ---------------------------------------------------
    def test_normal_borrow1(self):
        # 준비된 데이터로 테스트 컨텍스트 생성
        app = self.prepare_test_context(
            file_data={
                "users": ["U001|John Doe|1234|"],
                "books": ["001|ISBN01"],
                "isbn": ["ISBN01|Python Basics|Alice|CAT00"],
                "cats": ["CAT00|general"],
                "borrow": [],
                "borrow_hist": [],
            },
            current_user=User("U001", "John Doe", "1234", ""),
            current_date=datetime(2025, 1, 1),
        )
        book_service = BookService(app)
        borrow_service = BorrowService(app)
        
        # borrow_prompt 실행
        output = self.execute_borrow_prompt(book_service, borrow_service, input_values=["001"])
        # 결과 검증
        self.assert_after_prompt(
            output,
            expected_output_keywords=["Python Basics", "대출되었습니다"],
            file_expect_contains={"borrow": ["001|U001"]},
            file_expect_not_contains={"borrow": ["U999"]},
        )
    def test_normal_borrow2(self):
        # 준비된 데이터로 테스트 컨텍스트 생성
        app = self.prepare_test_context(
            file_data={
                "users": ["U001|John Doe|1234|"],
                "books": ["001|ISBN01"],
                "isbn": ["ISBN01|Python Basics|Alice|CAT00"],
                "cats": ["CAT00|general"],
                "borrow": [],
                "borrow_hist": [],
            },
            current_user=User("U001", "John Doe", "1234", ""),
            current_date=datetime(2025, 1, 1),
        )
        book_service = BookService(app)
        borrow_service = BorrowService(app)
        
        # borrow_prompt 실행
        output = self.execute_borrow_prompt(book_service, borrow_service, input_values=["001"])
        # 결과 검증
        self.assert_after_prompt(
            output,
            expected_output_keywords=["Python Basics", "대출되었습니다"],
            file_expect_contains={"borrow": ["001|U001"]},
            file_expect_not_contains={"borrow": ["U999"]},
        )

    def test_borrow_already_borrowed(self):
        app = self.prepare_test_context(
            file_data={
                "users": ["U001|John Doe|1234|"],
                "books": ["001|ISBN01"],
                "isbn": ["ISBN01|Python Basics|Alice|CAT00"],
                "cats": ["CAT00|general"],
                "borrow": ["001|U999|2025-01-01|2025-01-08"],  # 이미 다른 사람이 대출한 상태
                "borrow_hist": [],
            },
            current_user=User("U001", "John Doe", "1234", ""),
            current_date=datetime(2025, 1, 1),
        )
        book_service = BookService(app)
        borrow_service = BorrowService(app)

        # borrow_prompt 실행
        output = self.execute_borrow_prompt(book_service, borrow_service, input_values=["001"])

        self.assert_after_prompt(
            output,
            expected_output_keywords=["이미 대출중인 도서"],
            file_expect_not_contains={"borrow": ["U001|"]}
        )
    def test_borrow_limit_exceeded(self):
        app = self.prepare_test_context(
            file_data={
                "users": ["U001|John Doe|1234|"],
                "books": ["004|ISBN01"],
                "isbn": ["ISBN01|Python Basics|Alice|CAT00"],
                "cats": ["CAT00|general"],
                "borrow": [
                    "001|U001|2025-01-01|2025-01-08",
                    "002|U001|2025-01-01|2025-01-08",
                    "003|U001|2025-01-01|2025-01-08",  # 이미 3권 대출 상태
                ],
                "borrow_hist": [],
            },
            current_user=User("U001", "John Doe", "1234", ""),
            current_date=datetime(2025, 1, 1),
        )
        book_service = BookService(app)
        borrow_service = BorrowService(app)

        # borrow_prompt 실행
        output = self.execute_borrow_prompt(book_service, borrow_service, input_values=["004"])

        self.assert_after_prompt(
            output,
            expected_output_keywords=["대출 가능 한도를 초과했습니다"],  # 현재 코드 메시지 기준
            file_expect_not_contains={"borrow": ["004|U001"]},
        )

    def test_borrow_invalid_book_id(self):
        app = self.prepare_test_context(
            file_data={
                "users": ["U001|John Doe|1234|"],
                "books": ["001|ISBN01"],  # 999 없음
                "isbn": ["ISBN01|Python Basics|Alice|CAT00"],
                "cats": ["CAT00|general"],
                "borrow": [],
                "borrow_hist": [],
            },
            current_user=User("U001", "John Doe", "1234", ""),
            current_date=datetime(2025, 1, 1),
        )
        book_service = BookService(app)
        borrow_service = BorrowService(app)

        # borrow_prompt 실행
        output = self.execute_borrow_prompt(book_service, borrow_service, input_values=["999"])

        self.assert_after_prompt(
            output,
            expected_output_keywords=["존재하지 않는 고유번호"],
            file_expect_not_contains={"borrow": ["999"]},
        )
    def test_penalty_user_already_borrowed(self):
        app = self.prepare_test_context(
            file_data={
                "users": ["U001|John Doe|1234|2025-11-30"],   # penalty 존재
                "books": ["043|ISBN43"],
                "isbn": ["ISBN43|SomeBook|AuthorX|CAT00"],
                "cats": ["CAT00|general"],
                "borrow": ["001|U001|2025-01-01|2025-01-08"],  # 이미 1권 대출
                "borrow_hist": [],
            },
            current_user=User("U001", "John Doe", "1234", "2025-11-30"),
            current_date=datetime(2025, 1, 1),
        )
        book_service = BookService(app)
        borrow_service = BorrowService(app)

        # borrow_prompt 실행
        output = self.execute_borrow_prompt(book_service, borrow_service, input_values=["043"])
        print(f"output:\n{output}")
        self.assert_after_prompt(
            output,
            expected_output_keywords=[
                "제재 상태에서는 책을 1권 이상 빌릴 수 없습니다",
                "2025-11-30"
            ],
            file_expect_not_contains={"borrow": ["043|U001"]},
        )

    def test_user_has_overdue_book(self):
        app = self.prepare_test_context(
            file_data={
                "users": ["U001|John Doe|1234|"],
                "books": ["020|ISBN20"],
                "isbn": ["ISBN20|SomeBook|AuthorX|CAT00"],
                "cats": ["CAT00|general"],
                "borrow": ["001|U001|2025-01-01|2025-01-05"],  # due_date 지남 → 연체
                "borrow_hist": [],
            },
            current_user=User("U001", "John Doe", "1234", ""),
            current_date=datetime(2025, 1, 10),  # 현재 날짜가 overdue 상태
        )
        book_service = BookService(app)
        borrow_service = BorrowService(app)

        # borrow_prompt 실행
        output = self.execute_borrow_prompt(book_service, borrow_service, input_values=["020"])

        self.assert_after_prompt(
            output,
            expected_output_keywords=[
                "연체중인 도서가 존재합니다!! 반납 후 이용해 주세요."
            ],
            file_expect_not_contains={"borrow": ["020|U001"]},
        )

    def test_user_has_overdue_book(self):
        app = self.prepare_test_context(
            file_data={
                "users": ["U001|John Doe|1234|"],
                "books": ["020|ISBN20"],
                "isbn": ["ISBN20|SomeBook|AuthorX|CAT00"],
                "cats": ["CAT00|general"],
                "borrow": ["001|U001|2025-01-01|2025-01-05"],  # due_date 지남 → 연체
                "borrow_hist": [],
            },
            current_user=User("U001", "John Doe", "1234", ""),
            current_date=datetime(2025, 1, 10),  # 현재 날짜가 overdue 상태
        )
        book_service = BookService(app)
        borrow_service = BorrowService(app)

        # borrow_prompt 실행
        output = self.execute_borrow_prompt(book_service, borrow_service, input_values=["020"])

        self.assert_after_prompt(
            output,
            expected_output_keywords=[
                "연체중인 도서가 존재합니다!! 반납 후 이용해 주세요."
            ],
            file_expect_not_contains={"borrow": ["020|U001"]},
        )

    def test_borrow_limit_exceeded_per_plan(self):
        app = self.prepare_test_context(
            file_data={
                "users": ["U001|John Doe|1234|"],
                "books": ["023|ISBN23"],
                "isbn": ["ISBN23|SomeBook|AuthorX|CAT00"],
                "cats": ["CAT00|general"],
                "borrow": [
                    "001|U001|2025-01-01|2025-01-08",
                    "002|U001|2025-01-01|2025-01-08",
                    "003|U001|2025-01-01|2025-01-08",
                ],  # 이미 3권
                "borrow_hist": [],
            },
            current_user=User("U001", "John Doe", "1234", ""),
            current_date=datetime(2025, 1, 1),
        )
        book_service = BookService(app)
        borrow_service = BorrowService(app)

        # borrow_prompt 실행
        output = self.execute_borrow_prompt(book_service, borrow_service, input_values=["023"])

        self.assert_after_prompt(
            output,
            expected_output_keywords=[
                "대출 가능 한도를 초과했습니다!! 다음에 이용해 주세요."
            ],
            file_expect_not_contains={"borrow": ["023|U001"]},
        )



class ReturnPromptTest(PromptTestBase):
    ENABLE_FILE_PRINT = True   # 확인용 출력 ON/OFF
    ENABLE_FILE_CLEANUP = True # 테스트 파일 삭제 ON/OFF

    # borrow_prompt 실행 + 출력 캡처
    def execute_return_prompt(self, book_service, borrow_service, input_values):
        return self.execute_prompt(
            input_values, return_prompt,
            book_service=book_service, borrow_service=borrow_service
        )

    def test_return_normal(self):
        app = self.prepare_test_context(
            file_data={
                "users": ["U001|John Doe|1234|"],
                "books": ["001|ISBN01"],
                "isbn": ["ISBN01|Python Basics|Alice|CAT00"],
                "cats": ["CAT00|general"],
                "borrow": ["001|U001|2025-01-01|2025-01-08"],
                "borrow_hist": [],
            },
            current_user=User("U001", "John Doe", "1234", ""),
            current_date=datetime(2025, 1, 5),
        )
        book_service = BookService(app)
        borrow_service = BorrowService(app)

        # input: bookID, yes
        output = self.execute_return_prompt(book_service, borrow_service, ["001", "Y"])

        self.assert_after_prompt(
            output,
            expected_output_keywords=["정상적으로 반납이 완료되었습니다"],
            file_expect_contains={"borrow_hist": ["001|U001"]},
            file_expect_not_contains={"borrow": ["001|U001"]},
        )

    def test_return_no_borrowed_books(self):
        app = self.prepare_test_context(
            file_data={
                "users": ["U001|John Doe|1234|"],
                "books": ["001|ISBN01"],
                "isbn": ["ISBN01|Python Basics|Alice|CAT00"],
                "cats": ["CAT00|general"],
                "borrow": [],  # 대출 없음
                "borrow_hist": [],
            },
            current_user=User("U001", "John Doe", "1234", ""),
            current_date=datetime(2025, 1, 5),
        )

        book_service = BookService(app)
        borrow_service = BorrowService(app)

        output = self.execute_return_prompt(book_service, borrow_service, [])

        self.assert_after_prompt(
            output,
            expected_output_keywords=["현재 대출한 도서가 없습니다"],
        )

    def test_return_invalid_book_id(self):
        app = self.prepare_test_context(
            file_data={
                "users": ["U001|John Doe|1234|"],
                "books": ["001|ISBN01"],
                "isbn": ["ISBN01|Python Basics|Alice|CAT00"],
                "cats": ["CAT00|general"],
                "borrow": ["001|U001|2025-01-01|2025-01-08"],
                "borrow_hist": [],
            },
            current_user=User("U001", "John Doe", "1234", ""),
            current_date=datetime(2025, 1, 5),
        )

        book_service = BookService(app)
        borrow_service = BorrowService(app)

        output = self.execute_return_prompt(book_service, borrow_service, ["999"])

        self.assert_after_prompt(
            output,
            expected_output_keywords=["잘못된 값을 입력했습니다"],
            file_expect_contains={"borrow": ["001|U001"]},  # 반납 안됨
        )

    def test_return_user_cancel(self):
        app = self.prepare_test_context(
            file_data={
                "users": ["U001|John Doe|1234|"],
                "books": ["001|ISBN01"],
                "isbn": ["ISBN01|Python Basics|Alice|CAT00"],
                "cats": ["CAT00|general"],
                "borrow": ["001|U001|2025-01-01|2025-01-08"],
                "borrow_hist": [],
            },
            current_user=User("U001", "John Doe", "1234", ""),
            current_date=datetime(2025, 1, 5),
        )

        book_service = BookService(app)
        borrow_service = BorrowService(app)

        output = self.execute_return_prompt(book_service, borrow_service, ["001", "N"])

        self.assert_after_prompt(
            output,
            expected_output_keywords=["사용자가 반납을 취소했습니다"],
            file_expect_contains={"borrow": ["001|U001"]},  # 여전히 존재해야 함
            file_expect_not_contains={"borrow_hist": ["001|U001"]},
        )

    def test_return_display_borrow_list(self):
        app = self.prepare_test_context(
            file_data={
                "users": ["U001|John Doe|1234|"],
                "books": ["001|ISBN01"],
                "isbn": ["ISBN01|Python Basics|Alice|CAT00"],
                "cats": ["CAT00|general"],
                "borrow": ["001|U001|2025-01-01|2025-01-08"],
                "borrow_hist": [],
            },
            current_user=User("U001", "John Doe", "1234", ""),
            current_date=datetime(2025, 1, 5),
        )

        book_service = BookService(app)
        borrow_service = BorrowService(app)

        # 반납 절차 시작 (목록 출력 포함)
        output = self.execute_return_prompt(book_service, borrow_service, ["001", "Y"])

        # UI 검증
        self.assertIn("제목: Python Basics", output)
        self.assertIn("저자: Alice", output)

class ReturnPromptPenaltyTest(PromptTestBase):
    ENABLE_FILE_PRINT = True   # 확인용 출력 ON/OFF
    ENABLE_FILE_CLEANUP = True # 테스트 파일 삭제 ON/OFF


    def execute_return_prompt(self, book_service, borrow_service, input_values):
        return self.execute_prompt(
            input_values, return_prompt,
            book_service=book_service, borrow_service=borrow_service
        )

    def read_user_penalty(self):
        content = open(self.paths["users"]).read().strip()
        return content.split("|")[3]  # penaltyDate position

    # -----------------------------------------------------
    # 1) penalty 없음 + 연체 없음 (변경 없음)
    # -----------------------------------------------------
    def test_penalty_none_no_overdue(self):
        today = datetime(2025, 1, 10)

        app = self.prepare_test_context(
            file_data={
                "users": ["U001|John Doe|1234|"],
                "books": ["001|ISBN01"],
                "isbn": ["ISBN01|Book|Author|CAT00"],
                "cats": ["CAT00|general"],
                "borrow": ["001|U001|2025-01-08|2025-01-10"],
                "borrow_hist": [],
            },
            current_user=User("U001", "John Doe", "1234", ""),
            current_date=today,
        )

        book_service = BookService(app)
        borrow_service = BorrowService(app)

        self.execute_return_prompt(book_service, borrow_service, ["001", "Y"])

        penalty = self.read_user_penalty()
        assert penalty == ""

    # -----------------------------------------------------
    # 2) penalty 없음 + 연체 5일 → today + 5
    # -----------------------------------------------------
    def test_penalty_none_overdue_5(self):
        today = datetime(2025, 1, 10)

        app = self.prepare_test_context(
            file_data={
                "users": ["U001|John Doe|1234|"],
                "books": ["001|ISBN01"],
                "isbn": ["ISBN01|Book|Auth|CAT00"],
                "cats": ["CAT00|general"],
                "borrow": ["001|U001|2025-01-01|2025-01-05"],
                "borrow_hist": [],
            },
            current_user=User("U001", "John Doe", "1234", ""),
            current_date=today,
        )

        book_service = BookService(app)
        borrow_service = BorrowService(app)

        self.execute_return_prompt(book_service, borrow_service, ["001", "Y"])
        penalty = self.read_user_penalty()

        assert penalty == "2025-01-15"

    # -----------------------------------------------------
    # 3) 기존 penalty 과거 + overdue 없음 → 변경 없음
    # -----------------------------------------------------
    def test_penalty_past_no_overdue(self):
        today = datetime(2025, 2, 1)

        app = self.prepare_test_context(
            file_data={
                "users": ["U001|John Doe|1234|2025-01-10"],
                "books": ["001|ISBN01"],
                "isbn": ["ISBN01|Book|Auth|CAT00"],
                "cats": ["CAT00|general"],
                "borrow": ["001|U001|2025-01-25|2025-02-01"],
                "borrow_hist": [],
            },
            current_user=User("U001", "John Doe", "1234", "2025-01-10"),
            current_date=today,
        )

        book_service = BookService(app)
        borrow_service = BorrowService(app)

        self.execute_return_prompt(book_service, borrow_service, ["001", "Y"])
        penalty = self.read_user_penalty()

        assert penalty == "2025-01-10"

    # -----------------------------------------------------
    # 4) penalty 미래 + overdue 없음 → 유지
    # -----------------------------------------------------
    def test_penalty_future_no_overdue(self):
        today = datetime(2025, 1, 10)

        app = self.prepare_test_context(
            file_data={
                "users": ["U001|John Doe|1234|2025-02-01"],
                "books": ["001|ISBN01"],
                "isbn": ["ISBN01|Book|Auth|CAT00"],
                "cats": ["CAT00|general"],
                "borrow": ["001|U001|2025-01-05|2025-01-10"],
                "borrow_hist": [],
            },
            current_user=User("U001", "John Doe", "1234", "2025-02-01"),
            current_date=today,
        )

        book_service = BookService(app)
        borrow_service = BorrowService(app)

        self.execute_return_prompt(book_service, borrow_service, ["001", "Y"])
        penalty = self.read_user_penalty()

        assert penalty == "2025-02-01"

    # -----------------------------------------------------
    # 5) penalty 과거 + overdue 3 → today + 3
    # -----------------------------------------------------
    def test_penalty_past_overdue_3(self):
        today = datetime(2025, 1, 20)

        app = self.prepare_test_context(
            file_data={
                "users": ["U001|John Doe|1234|2025-01-10"],
                "books": ["001|ISBN01"],
                "isbn": ["ISBN01|Book|Auth|CAT00"],
                "cats": ["CAT00|general"],
                "borrow": ["001|U001|2025-01-01|2025-01-17"],
                "borrow_hist": [],
            },
            current_user=User("U001", "John Doe", "1234", "2025-01-10"),
            current_date=today,
        )

        book_service = BookService(app)
        borrow_service = BorrowService(app)

        self.execute_return_prompt(book_service, borrow_service, ["001", "Y"])
        penalty = self.read_user_penalty()

        assert penalty == "2025-01-23"

    # -----------------------------------------------------
    # 6) penalty 미래 + overdue 4 → penalty + 4
    # -----------------------------------------------------
    def test_penalty_future_overdue_4(self):
        today = datetime(2025, 1, 10)

        app = self.prepare_test_context(
            file_data={
                "users": ["U001|John Doe|1234|2025-01-20"],
                "books": ["001|ISBN01"],
                "isbn": ["ISBN01|Book|Auth|CAT00"],
                "cats": ["CAT00|general"],
                "borrow": ["001|U001|2025-01-01|2025-01-06"],
                "borrow_hist": [],
            },
            current_user=User("U001", "John Doe", "1234", "2025-01-20"),
            current_date=today,
        )

        book_service = BookService(app)
        borrow_service = BorrowService(app)

        self.execute_return_prompt(book_service, borrow_service, ["001", "Y"])
        penalty = self.read_user_penalty()

        assert penalty == "2025-01-24"

    # -----------------------------------------------------
    # 7) penalty 날짜가 유효한 실제 날짜여야 함
    # -----------------------------------------------------
    def test_penalty_date_must_be_valid(self):
        today = datetime(2025, 2, 25)

        app = self.prepare_test_context(
            file_data={
                "users": ["U001|John Doe|1234|2025-02-27"],
                "books": ["001|ISBN01"],
                "isbn": ["ISBN01|Book|Auth|CAT00"],
                "cats": ["CAT00|general"],
                "borrow": ["001|U001|2025-02-01|2025-02-24"],
                "borrow_hist": [],
            },
            current_user=User("U001", "John Doe", "1234", "2025-02-27"),
            current_date=today,
        )

        book_service = BookService(app)
        borrow_service = BorrowService(app)

        self.execute_return_prompt(book_service, borrow_service, ["001", "Y"])
        penalty = self.read_user_penalty()

        assert penalty == "2025-02-28"  # 실제 존재하는 날짜

    # -----------------------------------------------------
    # 8) today == penalty + overdue
    # -----------------------------------------------------
    def test_penalty_today_equal_penalty(self):
        today = datetime(2025, 1, 10)

        app = self.prepare_test_context(
            file_data={
                "users": ["U001|John Doe|1234|2025-01-10"],
                "books": ["001|ISBN01"],
                "isbn": ["ISBN01|Book|Auth|CAT00"],
                "cats": ["CAT00|general"],
                "borrow": ["001|U001|2025-01-01|2025-01-08"],
                "borrow_hist": [],
            },
            current_user=User("U001", "John Doe", "1234", "2025-01-10"),
            current_date=today,
        )

        book_service = BookService(app)
        borrow_service = BorrowService(app)

        self.execute_return_prompt(book_service, borrow_service, ["001", "Y"])
        penalty = self.read_user_penalty()

        assert penalty == "2025-01-12"

    # -----------------------------------------------------
    # 9) overdue 음수 → 0으로 처리
    # -----------------------------------------------------
    def test_penalty_negative_overdue_treated_as_zero(self):
        today = datetime(2025, 1, 10)

        app = self.prepare_test_context(
            file_data={
                "users": ["U001|John Doe|1234|"],
                "books": ["001|ISBN01"],
                "isbn": ["ISBN01|Book|Auth|CAT00"],
                "cats": ["CAT00|general"],
                "borrow": ["001|U001|2025-01-09|2025-01-12"],
                "borrow_hist": [],
            },
            current_user=User("U001", "John Doe", "1234", ""),
            current_date=today,
        )

        book_service = BookService(app)
        borrow_service = BorrowService(app)

        self.execute_return_prompt(book_service, borrow_service, ["001", "Y"])
        penalty = self.read_user_penalty()

        assert penalty == ""

