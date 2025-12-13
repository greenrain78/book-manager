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

    # def test_1(self):
    #     # 파일 준비
    #     app = self.prepare_test_context(
    #         file_data={
    #             "users": ["java|12341234|test@gmail.com|"],
    #             "books": ["001|ISBN01"],
    #             "isbn": ["ISBN01|Python Basics|Alice|CAT00"],
    #             "cats": ["CAT00|general"],
    #             "borrow": [],
    #             "borrow_hist": [],
    #         },
    #     )
    #     # 실행 및 입력값 제공
    #     output = self.execute_app(
    #         app=app, input_values=[
    #             "2020-11-11",  # 프로그램 시작 날짜
    #             "2",        # 로그인
    #             "java",    # 아이디
    #             "4",        # 로그아웃
    #             "3",        # 종료
    #
    #         ])
    #     # 결과 검증
    #     self.assert_after_prompt(
    #         output,
    #         expected_output_keywords=[
    #             " ",
    #         ],
    #     )

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


    def test_4(self):
        # 파일 준비
        app = self.prepare_test_context(
            file_data={
                "users": ["java|12341234|test@gmail.com|", "admin|12341234|123@gmail.com|"],
                "books": [
                    "001|ISBN01", "002|ISBN01", "003|ISBN01", "004|ISBN01", "005|ISBN01", "006|ISBN01", "007|ISBN01",
                    "008|ISBN01", "009|ISBN01", "010|ISBN01", "011|ISBN01", "012|ISBN01", "013|ISBN01", "014|ISBN01",
                    "015|ISBN01", "016|ISBN01", "017|ISBN01", "018|ISBN01", "019|ISBN01", "020|ISBN01",
                ],
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
                "admin",    # 아이디
                "12341234", # 비밀번호
                "1",        # 도서 추가
                # 등록될 수 있는 책은 총 20권입니다. 더이상 추가 할 수 없습니다.
                "5"       # 로그아웃
                "3",        # 종료
            ])
        # 결과 검증
        self.assert_after_prompt(
            output,
            expected_output_keywords=[
                "등록될 수 있는 책은 총 20권입니다. 더이상 추가 할 수 없습니다."
            ],

        )

    def test_5(self):
        # 파일 준비
        app = self.prepare_test_context(
            file_data={
                "users": ["java|12341234|test@gmail.com|", "admin|12341234|123@gmail.com|"],
                "books": [
                    "001|ISBN01",
                ],
                "isbn": ["ISBN01|Python Basics|Alice|CAT00"],
                "cats": ["CAT00|general"],
                "borrow": [],
                "borrow_hist": [
                    "001|gw5621|2025-01-01|2025-01-08|2025-01-01",
                    "002|gw5621|2025-01-01|2025-01-08|2025-02-01",
                    "003|gw5621|2025-01-01|2025-01-08|2025-02-01",
                ],
            },
        )
        # 실행 및 입력값 제공
        output = self.execute_app(
            app=app, input_values=[
                "2025-02-11",  # 프로그램 시작 날짜
            ])
        # 결과 검증
        self.assert_after_prompt(
            output,
            expected_output_keywords=[
                " "
            ],

        )