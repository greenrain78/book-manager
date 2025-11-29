from datetime import timedelta
from logging import getLogger
from typing import Optional

from src.controller.prompt import PromptType
from src.core.valid import check_disk_space
from src.prompt.menu import main_prompt
from src.prompt.search import search_by_book_prompt
from src.prompt.start import login_prompt, signup_prompt
from src.prompt.user import user_prompt, search_prompt
from src.repository.entity import User
from src.repository.manager import UsersRepository, BooksRepository, BorrowHistoryRepository, BorrowRepository, \
    ISBNRepository, CategoryRepository
from src.service.book_service import BookService
from src.service.user_service import UserService
from src.settings import BORROW_HISTORY_DATA_PATH, BORROW_DATA_PATH, BOOK_DATA_PATH, USER_DATA_PATH, BORROW_PERIOD_DAYS, \
    ISBN_DATA_PATH, CATEGORY_DATA_PATH

log = getLogger(__name__)


class AppContext:
    borrow_period = timedelta(days=BORROW_PERIOD_DAYS)

    def __init__(self):
        self.current_date = None
        self.current_user: Optional[User] = None

        # 시스템 요구사항 확인
        self.check_system_requirements()
        # 리포지토리 초기화
        try:
            users_repo: UsersRepository = UsersRepository(path=USER_DATA_PATH)
            books_repo: BooksRepository = BooksRepository(path=BOOK_DATA_PATH)
            borrow_repo: BorrowRepository = BorrowRepository(path=BORROW_DATA_PATH)
            borrow_history_repo: BorrowHistoryRepository = BorrowHistoryRepository(path=BORROW_HISTORY_DATA_PATH)
            isbn_repo: ISBNRepository = ISBNRepository(path=ISBN_DATA_PATH)
            cat_repo: CategoryRepository = CategoryRepository(path=CATEGORY_DATA_PATH)

            self.book_service = BookService(
                books_repo=books_repo,
                isbn_repo=isbn_repo,
                cat_repo=cat_repo,
                borrow_repo=borrow_repo
            )
            self.user_service = UserService(
                user_repo=users_repo,
            )
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

    def start(self):
        next_prompt = PromptType.MAIN_MENU

        while True:
            if next_prompt == PromptType.USER_MENU:
                next_prompt = user_prompt()

            elif next_prompt == PromptType.SEARCH_MENU:
                next_prompt = search_prompt()

            elif next_prompt == PromptType.SEARCH_BOOK:
                search_by_book_prompt(service=self.book_service)
                next_prompt = PromptType.SEARCH_MENU

            elif next_prompt == PromptType.EXIT:
                break

            elif next_prompt == PromptType.MAIN_MENU:
                next_prompt = main_prompt()

            elif next_prompt == PromptType.LOGIN:
                next_prompt = login_prompt(user_service=self.user_service, app=self)

            elif next_prompt == PromptType.SIGNUP:
                next_prompt = signup_prompt(user_service=self.user_service)


            # elif next_prompt == PromptType.SEARCH_CATEGORY:
            #     search_by_category_prompt()
            #     next_prompt = PromptType.SEARCH_MENU
            #
            # elif next_prompt == PromptType.BORROW:
            #     self.main_controller.book_borrow()
            #     next_prompt = PromptType.USER_MENU
            #
            # elif next_prompt == PromptType.RETURN:
            #     self.main_controller.book_return()
            #     next_prompt = PromptType.USER_MENU
            #
            # elif next_prompt == PromptType.LOGOUT:
            #     self.main_controller.user_logout()
            #     break

        log.info("프로그램을 종료합니다.")