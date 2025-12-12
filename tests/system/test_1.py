from src.prompt.user import borrow_prompt
from tests.common import SystemTestBase


class SystemTest1(SystemTestBase):
    ENABLE_FILE_PRINT = True  # 확인용 출력 ON/OFF
    ENABLE_FILE_CLEANUP = True  # 테스트 파일 삭제 ON/OFF

    # borrow_prompt 실행 + 출력 캡처
    def execute_borrow_prompt(self, book_service, borrow_service, input_values):
        return self.execute_prompt(
            input_values, borrow_prompt,
            book_service=book_service, borrow_service=borrow_service
        )

    def test_1(self):
        # 파일 준비
        app = self.prepare_test_context(
            file_data={
                "users": ["java|1234|test@gmail.com|"],
                "books": ["001|ISBN01"],
                "isbn": ["ISBN01|Python Basics|Alice|CAT00"],
                "cats": ["CAT00|general"],
                "borrow": [],
                "borrow_hist": [],
            },
        )
        # 실행 및 입력값 제공
        output = self.execute_app(
            app=app, input_values=[
                "2020-11-11",  # 프로그램 시작 날짜
                "2",        # 로그인
                "java1",    # 아이디
            ])
        # 결과 검증
        self.assert_after_prompt(
            output,
            expected_output_keywords=[
                "존재하지 않는 ID입니다!!  ID를 다시 입력하세요.",
            ],
            file_expect_contains={"users": ["java"]},
            file_expect_not_contains={"users": ["java1"]}
        )

    def test_2(self):
        # 파일 준비
        app = self.prepare_test_context(
            file_data={
                "users": ["java|12341234|test@gmail.com|"],
                "books": ["001|ISBN01"],
                "isbn": ["ISBN01|Python Basics|Alice|CAT00"],
                "cats": ["CAT00|general"],
                "borrow": [],
                "borrow_hist": [],
            },
        )
        # 실행 및 입력값 제공
        output = self.execute_app(
            app=app, input_values=[
                "2020-11-11",  # 프로그램 시작 날짜
                "2",        # 로그인
                "java",    # 아이디
                "12341234", # 비밀번호
                "1",        # 도서 검색
                "1",        # 도서명으로 검색
                "Python", # 도서명
                "4",        # 로그아웃
                "3",        # 종료

            ])
        # 결과 검증
        self.assert_after_prompt(
            output,
            expected_output_keywords=[
                "대여가능 ",
            ],
        )


    def test_3(self):
        # 파일 준비
        app = self.prepare_test_context(
            file_data={
                "users": ["java|12341234|test@gmail.com|"],
                "books": ["001|ISBN01"],
                "isbn": ["ISBN01|Python Basics|Alice|CAT00"],
                "cats": ["CAT00|general"],
                "borrow": [],
                "borrow_hist": [],
            },
        )
        # 실행 및 입력값 제공
        output = self.execute_app(
            app=app, input_values=[
                "2020-11-11",  # 프로그램 시작 날짜
                "2",        # 로그인
                "java",    # 아이디
                "12341234", # 비밀번호
                "1",        # 도서 검색
                "1",        # 도서명으로 검색
                " Python", # 도서명
                "4",        # 로그아웃
                "3",        # 종료

            ])
        # 결과 검증
        self.assert_after_prompt(
            output,
            expected_output_keywords=[
                "현재 대출한 도서가 없습니다."
            ],
            expected_output_not_keywords=[
                "대여가능",
            ],
        )