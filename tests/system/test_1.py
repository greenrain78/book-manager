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
    #             "cats": ["CAT00|uncategorized"],
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
                "cats": ["CAT00|uncategorized"],
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
                "cats": ["CAT00|uncategorized"],
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
                "cats": ["CAT00|uncategorized"],
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
                "cats": ["CAT00|uncategorized"],
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

    def test_6(self):
        # 파일 준비
        app = self.prepare_test_context(
            file_data={
                "users": ["java|12341234|test@gmail.com|", "admin|12341234|123@gmail.com|"],
                "books": [
                    "001|ISBN01",
                ],
                "isbn": ["ISBN01|Python Basics|Alice|CAT00"],
                "cats": ["CAT00|uncategorized"],
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
                "3",        # 도서 수정
                "ISBN99",   # 존재하지 않는 ISBN
                "5"       # 로그아웃
                "3",        # 종료
            ])
        # 결과 검증
        self.assert_after_prompt(
            output,
            expected_output_keywords=[
                "존재하지 않는 ISBN입니다."
            ],

        )
    def test_7(self):
        # 파일 준비
        app = self.prepare_test_context(
            file_data={
                "users": ["java|12341234|test@gmail.com|", "admin|12341234|123@gmail.com|"],
                "books": [
                    "001|ISBN01",
                ],
                "isbn": ["ISBN01|Python Basics|Alice|CAT00"],
                "cats": ["CAT00|uncategorized"],
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
                "2",        # 도서 삭제
                "001 ",   # 공백 포함된 book_id
                "001",  # book_id
                "n",
                "5",       # 로그아웃
                "3",        # 종료
            ])
        # 결과 검증
        self.assert_after_prompt(
            output,
            expected_output_keywords=[
                "고유번호는 공백을 포함하지 않습니다"
            ],

        )

    def test_8(self):
        # 파일 준비
        app = self.prepare_test_context(
            file_data={
                "users": ["java|12341234|test@gmail.com|", "admin|12341234|123@gmail.com|"],
                "books": [
                    "001|ISBN01",
                ],
                "isbn": ["ISBN01|Python Basics|Alice|CAT00"],
                "cats": ["CAT00|uncategorized"],
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
                "3",        # 도서 수정
                "ISBN01",   # 존재하는 ISBN
                " Python|taewoon", # 공백이 포함된 제목과 저자
                "Python|Alice", # 올바른 제목과 저자
                "5",       # 로그아웃
                "3",        # 종료
            ])
        # 결과 검증
        self.assert_after_prompt(
            output,
            expected_output_keywords=[
                "잘못된 입력입니다!! 올바른 제목을 입력하세요."
            ],

        )

    def test_9(self):
        # 파일 준비
        app = self.prepare_test_context(
            file_data={
                "users": ["java|12341234|test@gmail.com|", "admin|12341234|123@gmail.com|"],
                "books": [
                    "001|ISBN01",
                ],
                "isbn": ["ISBN01|Python Basics|Alice|CAT00"],
                "cats": [
                    "CAT00|uncategorized", "CAT01|science", "CAT02|space", "CAT03|history", "CAT04|art", "CAT05|technology",
                    "CAT06|mathematics", "CAT07|literature", "CAT08|philosophy", "CAT09|psychology", "CAT10|education",
                    "CAT11|health", "CAT12|travel", "CAT13|cooking", "CAT14|sports", "CAT15|business", "CAT16|economics",
                    "CAT17|politics", "CAT18|environment", "CAT19|culture", "CAT20|religion"
                ],
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
                "4",        # 카테고리 관리
                "1",        # 카테고리 추가
                "6"         # 뒤로가기
                "5",       # 로그아웃
                "3",        # 종료
            ])
        # 결과 검증
        self.assert_after_prompt(
            output,
            expected_output_keywords=[
                "카테고리가 너무 많습니다."
            ],

        )

    def test_10(self):
        # 파일 준비
        app = self.prepare_test_context(
            file_data={
                "users": ["java|12341234|test@gmail.com|", "admin|12341234|123@gmail.com|"],
                "books": [
                    "001|ISBN01",
                ],
                "isbn": ["ISBN01|Python Basics|Alice|CAT00"],
                "cats": ["CAT00|uncategorized"],
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
                "4",        # 카테고리 관리
                "7",        # 없음
                "6"         # 뒤로가기
                "5",       # 로그아웃
                "3",        # 종료
            ])
        # 결과 검증
        self.assert_after_prompt(
            output,
            expected_output_keywords=[
                "입력에 해당하는 명령어가 없습니다. 다시 입력해 주세요."
            ],
        )
    def test_11(self):
        # 파일 준비
        app = self.prepare_test_context(
            file_data={
                "users": ["java|12341234|test@gmail.com|", "admin|12341234|123@gmail.com|"],
                "books": [
                    "001|ISBN01",
                ],
                "isbn": ["ISBN01|Python Basics|Alice|CAT00"],
                "cats": ["CAT00|uncategorized"],
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
                "4",        # 카테고리 관리
                "1 1",        # 없음
                "6"         # 뒤로가기
                "5",       # 로그아웃
                "3",        # 종료
            ])
        # 결과 검증
        self.assert_after_prompt(
            output,
            expected_output_keywords=[
                "모든 명령어에는 인자가 필요하지 않습니다. 다시 입력해 주세요."
            ],
        )
    def test_12(self):
        # 파일 준비
        app = self.prepare_test_context(
            file_data={
                "users": ["java|12341234|test@gmail.com|", "admin|12341234|123@gmail.com|"],
                "books": [
                    "001|ISBN01",
                ],
                "isbn": ["ISBN01|Python Basics|Alice|CAT00"],
                "cats": ["CAT00|uncategorized"],
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
                "4",        # 카테고리 관리
                "5",        # 카테고리 부여
                # 부여할 카테고리가 없음
                "6",         # 뒤로가기
                "5",       # 로그아웃
                "3",        # 종료
            ])
        # 결과 검증
        self.assert_after_prompt(
            output,
            expected_output_keywords=[
                "카테고리가 너무 적습니다. 카테고리 추가하고 다시 시도해주세요."
            ],
        )

    def test_13(self):
        # 파일 준비
        app = self.prepare_test_context(
            file_data={
                "users": ["java|12341234|test@gmail.com|", "admin|12341234|123@gmail.com|"],
                "books": [
                    "001|ISBN01",
                ],
                "isbn": ["ISBN01|Python Basics|Alice|CAT00"],
                "cats": ["CAT00|uncategorized", "CAT01|computer"],
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
                "4",        # 카테고리 관리
                "2",        # 카테고리 삭제
                "math",
                "6",         # 뒤로가기
                "5",       # 로그아웃
                "3",        # 종료
            ])
        # 결과 검증
        self.assert_after_prompt(
            output,
            expected_output_keywords=[
                "존재하지 않는 카테고리입니다."
            ],
        )


    def test_14(self):
        # 파일 준비
        app = self.prepare_test_context(
            file_data={
                "users": ["java|12341234|test@gmail.com|", "admin|12341234|123@gmail.com|"],
                "books": [
                    "001|ISBN01",
                ],
                "isbn": ["ISBN01|papa|tae|CAT01"],
                "cats": ["CAT00|uncategorized", "CAT01|computer"],
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
                "4",        # 카테고리 관리
                "2",        # 카테고리 삭제
                "computer",
                "6",         # 뒤로가기
                "5",       # 로그아웃
                "3",        # 종료
            ])
        # 결과 검증
        self.assert_after_prompt(
            output,
            expected_output_keywords=[
                "해당 카테고리를 삭제했습니다."
            ],
            file_expect_contains={
                "isbn": ["ISBN01|papa|tae|CAT00"],
                "cats": ["CAT00|uncategorized"],
            }
        )


    def test_15(self):
        # 파일 준비
        app = self.prepare_test_context(
            file_data={
                "users": ["java|12341234|test@gmail.com|", "admin|12341234|123@gmail.com|"],
                "books": [
                    "001|ISBN01",
                ],
                "isbn": ["ISBN01|papa|tae|CAT01;CAT02"],
                "cats": ["CAT00|uncategorized", "CAT01|computer", "CAT02|math"],
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
                "4",        # 카테고리 관리
                "2",        # 카테고리 삭제
                "computer",
                "6",         # 뒤로가기
                "5",       # 로그아웃
                "3",        # 종료
            ])
        # 결과 검증
        self.assert_after_prompt(
            output,
            expected_output_keywords=[
                "해당 카테고리를 삭제했습니다."
            ],
            file_expect_contains={
                "isbn": ["ISBN01|papa|tae|CAT02"],
                "cats": ["CAT00|uncategorized"],
            },
            file_expect_not_contains={
                "cats": ["CAT01|computer"],
            }
        )


    def test_16(self):
        # 파일 준비
        app = self.prepare_test_context(
            file_data={
                "users": ["java|12341234|test@gmail.com|", "admin|12341234|123@gmail.com|"],
                "books": [
                    "001|ISBN01",
                ],
                "isbn": ["ISBN01|papa|tae|CAT01;CAT02;CAT03"],
                "cats": ["CAT00|uncategorized", "CAT01|computer", "CAT02|math", "CAT03|english"],
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
                "4",        # 카테고리 관리
                "2",        # 카테고리 삭제
                "computer",
                "6",         # 뒤로가기
                "5",       # 로그아웃
                "3",        # 종료
            ])
        # 결과 검증
        self.assert_after_prompt(
            output,
            expected_output_keywords=[
                "해당 카테고리를 삭제했습니다."
            ],
            file_expect_contains={
                "isbn": ["ISBN01|papa|tae|CAT02;CAT03"],
                "cats": ["CAT00|uncategorized"],
            },
            file_expect_not_contains={
                "cats": ["CAT01|computer"],
            }
        )
    def test_17(self):
        # 파일 준비
        app = self.prepare_test_context(
            file_data={
                "users": ["java|12341234|test@gmail.com|", "admin|12341234|123@gmail.com|"],
                "books": [
                    "001|ISBN01",
                ],
                "isbn": ["ISBN01|papa|tae|CAT01;CAT02;CAT03"],
                "cats": ["CAT00|uncategorized", "CAT01|computer"],
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
                "4",        # 카테고리 관리
                "1",        # 카테고리 추가
                "computer",
                "6",         # 뒤로가기
                "5",       # 로그아웃
                "3",        # 종료
            ])
        # 결과 검증
        self.assert_after_prompt(
            output,
            expected_output_keywords=[
                " "
            ],
        )


    def test_18(self):
        # 파일 준비
        app = self.prepare_test_context(
            file_data={
                "users": ["java|12341234|test@gmail.com|", "admin|12341234|123@gmail.com|"],
                "books": [
                    "001|ISBN01",
                ],
                "isbn": ["ISBN01|papa|tae|CAT01;CAT02;CAT03"],
                "cats": ["CAT00|uncategorized", "CAT01|computer"],
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
                "4",        # 카테고리 관리
                "4",        # 카테고리 수정
                "computer ",
                "6",         # 뒤로가기
                "5",       # 로그아웃
                "3",        # 종료
            ])
        # 결과 검증
        self.assert_after_prompt(
            output,
            expected_output_keywords=[
                "카테고리명은 공백을 포함하지않습니다. 다시 입력해주세요."
            ],
        )



    def test_19(self):
        # 파일 준비
        app = self.prepare_test_context(
            file_data={
                "users": ["java|12341234|test@gmail.com|", "admin|12341234|123@gmail.com|"],
                "books": [
                    "001|ISBN01",
                ],
                "isbn": ["ISBN01|papa|tae|CAT01;CAT02;CAT03"],
                "cats": ["CAT00|uncategorized", "CAT01|computer", "CAT02|math", "CAT03|english"],
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
                "4",        # 카테고리 관리
                "3",        # 카테고리 병합
                "computer",
                "math",
                "science",
                "6",         # 뒤로가기
                "5",       # 로그아웃
                "3",        # 종료
            ])
        # 결과 검증
        self.assert_after_prompt(
            output,
            expected_output_keywords=[
                "성공적으로 병합이 완료되었습니다."
            ],
            file_expect_contains={
                "isbn": ["ISBN01|papa|tae|CAT03;CAT04"],
                "cats": ["CAT00|uncategorized", "CAT03|english", "CAT04|science"],
            },
            file_expect_not_contains={
                "cats": ["CAT01|computer", "CAT02|math"],
            }
        )
    def test_20(self):
        # 파일 준비
        app = self.prepare_test_context(
            file_data={
                "users": ["java|12341234|test@gmail.com|", "admin|12341234|123@gmail.com|"],
                "books": [
                    "001|ISBN01",
                ],
                "isbn": ["ISBN01|papa|tae|CAT01;CAT02;CAT03"],
                "cats": ["CAT00|uncategorized", "CAT01|computer", "CAT02|math", "CAT03|english"],
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
                "4",        # 카테고리 관리
                "3",        # 카테고리 병합
                "computeraaaa", # 없는 카테고리
                "math",
                "science",
                "6",         # 뒤로가기
                "5",       # 로그아웃
                "3",        # 종료
            ])
        # 결과 검증
        self.assert_after_prompt(
            output,
            expected_output_keywords=[
                "존재하지 않는 카테고리명입니다. 다시 입력해주세요."
            ],
        )


    def test_21(self):
        # 파일 준비
        app = self.prepare_test_context(
            file_data={
                "users": ["java|12341234|test@gmail.com|", "admin|12341234|123@gmail.com|"],
                "books": [
                    "001|ISBN01",
                ],
                "isbn": ["ISBN01|papa|tae|CAT01;CAT02;CAT03"],
                "cats": ["CAT00|uncategorized", "CAT01|computer", "CAT02|math", "CAT03|english"],
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
                "2",        # 카테고리로 검색
                "com+aaa",  # + 기호는 없음
                "aaa", # 올바른 카테고리
                "4",       # 로그아웃
                "3",        # 종료
            ])
        # 결과 검증
        self.assert_after_prompt(
            output,
            expected_output_keywords=[
                "허용 가능한 연산자는 !,&,|입니다. 다시 입력해주세요."
            ],
        )


    def test_22(self):
        # 파일 준비
        app = self.prepare_test_context(
            file_data={
                "users": ["java|12341234|test@gmail.com|", "admin|12341234|123@gmail.com|"],
                "books": [
                    "001|ISBN01",
                ],
                "isbn": ["ISBN01|papa|tae|CAT01;CAT02;CAT03"],
                "cats": ["CAT00|uncategorized", "CAT01|computer", "CAT02|math", "CAT03|english"],
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
                "2",        # 카테고리로 검색
                "Com",  # 대문자
                "aaa", # 올바른 카테고리
                "4",       # 로그아웃
                "3",        # 종료
            ])
        # 결과 검증
        self.assert_after_prompt(
            output,
            expected_output_keywords=[
                "카테고리명은 로마자 소문자만 입력받을 수 있습니다. 다시 입력해주세요."
            ],
        )

    def test_23(self):
        # 파일 준비
        app = self.prepare_test_context(
            file_data={
                "users": ["java|12341234|test@gmail.com|", "admin|12341234|123@gmail.com|"],
                "books": [
                    "001|ISBN01",
                ],
                "isbn": ["ISBN01|papa|tae|CAT01;CAT02;CAT03"],
                "cats": ["CAT00|uncategorized", "CAT01|computer", "CAT02|math", "CAT03|english"],
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
                "2",        # 카테고리로 검색
                "aaa", # 없는 카테고리
                "4",       # 로그아웃
                "3",        # 종료
            ])
        # 결과 검증
        self.assert_after_prompt(
            output,
            expected_output_keywords=[
                "존재하지 않는 카테고리명입니다"
            ],
        )

    def test_24(self):
        # 파일 준비
        app = self.prepare_test_context(
            file_data={
                "users": ["java|12341234|test@gmail.com|", "admin|12341234|123@gmail.com|"],
                "books": [
                    "001|ISBN01",
                ],
                "isbn": ["ISBN01|papa|tae|CAT01;CAT02;CAT03"],
                "cats": ["CAT00|uncategorized", "CAT01|computer", "CAT02|math", "CAT03|english"],
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
                "4",        # 카테고리 관리
                "3",        # 카테고리 병합
                "computer", #
                "math",
                "english",
                "6",         # 뒤로가기
                "5",       # 로그아웃
                "3",        # 종료
            ])
        # 결과 검증
        self.assert_after_prompt(
            output,
            expected_output_keywords=[
                "이미 존재하는 카테고리명입니다. 다시 입력해주세요."
            ],
        )


    def test_25(self):
        # 파일 준비
        app = self.prepare_test_context(
            file_data={
                "users": ["java|12341234|test@gmail.com|", "admin|12341234|123@gmail.com|"],
                "books": [
                    "001|ISBN01",
                ],
                "isbn": ["ISBN01|papa|tae|CAT01;CAT02;CAT03"],
                "cats": ["CAT00|uncategorized", "CAT01|computer", "CAT02|math", "CAT03|english"],
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
                "4",        # 카테고리 관리
                "3",        # 카테고리 병합
                "computer", #
                "mathaa",   # 없는 카테고리
                "aaaa",     # 새로운 카테고리
                "6",         # 뒤로가기
                "5",       # 로그아웃
                "3",        # 종료
            ])
        # 결과 검증
        self.assert_after_prompt(
            output,
            expected_output_keywords=[
                "존재하지 않는 카테고리명입니다."
            ],
        )
    def test_26(self):
        # 파일 준비
        app = self.prepare_test_context(
            file_data={
                "users": ["java|12341234|test@gmail.com|", "admin|12341234|123@gmail.com|"],
                "books": [
                    "001|ISBN01",
                ],
                "isbn": ["ISBN01|papa|tae|CAT01;CAT02;CAT03"],
                "cats": ["CAT00|uncategorized", "CAT01|computer", "CAT02|math", "CAT03|english"],
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
                "4",        # 카테고리 관리
                "2",        # 카테고리 병합
                "uncategorized", #
                "6",         # 뒤로가기
                "5",       # 로그아웃
                "3",        # 종료
            ])
        # 결과 검증
        self.assert_after_prompt(
            output,
            expected_output_keywords=[
                "uncategorized는삭제할 수 없습니다."
            ],
        )

