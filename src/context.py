from datetime import timedelta
from logging import getLogger
from typing import Optional

from src.core.valid import check_disk_space
from src.repository.entity import User
from src.repository.manager import UsersRepository, BooksRepository, BorrowHistoryRepository, BorrowRepository, \
    ISBNRepository, CategoryRepository
from src.settings import BORROW_HISTORY_DATA_PATH, BORROW_DATA_PATH, BOOK_DATA_PATH, USER_DATA_PATH, BORROW_PERIOD_DAYS, \
    ISBN_DATA_PATH, CATEGORY_DATA_PATH

log = getLogger(__name__)


class AppContext:
    borrow_period = timedelta(days=BORROW_PERIOD_DAYS)

    def __init__(self):
        self.user_service = None
        self.borrow_service = None
        self.book_service = None
        self.current_date = None
        self.current_user: Optional[User] = None

        # 시스템 요구사항 확인
        self.check_system_requirements()
        # 리포지토리 초기화
        try:
            self.users_repo: UsersRepository = UsersRepository(path=USER_DATA_PATH)
            self.books_repo: BooksRepository = BooksRepository(path=BOOK_DATA_PATH)
            self.borrow_repo: BorrowRepository = BorrowRepository(path=BORROW_DATA_PATH)
            self.borrow_history_repo: BorrowHistoryRepository = BorrowHistoryRepository(path=BORROW_HISTORY_DATA_PATH)
            self.isbn_repo: ISBNRepository = ISBNRepository(path=ISBN_DATA_PATH)
            self.cat_repo: CategoryRepository = CategoryRepository(path=CATEGORY_DATA_PATH)
        except RuntimeError as e:
            self.exit_with_error(e)

    def check_system_requirements(self):
        # 디스크 공간 확인
        if not check_disk_space(required_mb=10, path="."):
            self.exit_with_error("필수 데이터 파일을 저장할 공간이 부족합니다. 디스크 용량 확인후 다시 시작해주세요.")

    def login(self, username, password):
        # 실제 애플리케이션에서는 데이터베이스 조회 등을 통해 인증을 수행합니다.
        # 여기서는 단순히 하드코딩된 사용자로 예시를 들겠습니다.
        if username == "admin" and password == "password":
            self.current_user = {"username": username}
            return True
        return False

    def logout(self):
        self.current_user = None

    def set_current_date(self, now_date):
        self.current_date = now_date

    def set_current_user(self, user: User):
        self.current_user = user

    @staticmethod
    def exit_with_error(msg):
        print(msg)
        input("Press Enter to continue...") # 사용자에게 메시지를 읽을 시간을 줌
        raise SystemExit

