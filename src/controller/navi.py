from logging import getLogger

from src.context import AppContext
from src.controller.prompt import PromptType
from src.prompt.admin import add_book_prompt
from src.prompt.menu import user_prompt, search_prompt, main_prompt, admin_prompt
from src.prompt.search import search_by_book_prompt, search_by_category_prompt
from src.prompt.start import login_prompt, signup_prompt
from src.service.book_service import BookService
from src.service.borrow_service import BorrowService
from src.service.user_service import UserService

log = getLogger(__name__)

class NavigationController:
    def __init__(
            self,
            app: AppContext,
        ):
        self.app = app
        self.book_service = BookService(app=app)
        self.user_service = UserService(app=app)
        self.borrow_service = BorrowService(app=app)

    def start(self):
        next_prompt = PromptType.MAIN_MENU

        while True:
            if next_prompt == PromptType.USER_MENU:
                next_prompt = user_prompt()

            elif next_prompt == PromptType.SEARCH_MENU:
                next_prompt = search_prompt()

            elif next_prompt == PromptType.SEARCH_BOOK:
                search_by_book_prompt(book_service=self.book_service, borrow_service=self.borrow_service)
                next_prompt = PromptType.SEARCH_MENU

            elif next_prompt == PromptType.EXIT:
                break

            elif next_prompt == PromptType.MAIN_MENU:
                next_prompt = main_prompt()

            elif next_prompt == PromptType.LOGIN:
                next_prompt = login_prompt(user_service=self.user_service, app=self.app)

            elif next_prompt == PromptType.SIGNUP:
                next_prompt = signup_prompt(user_service=self.user_service)

            elif next_prompt == PromptType.ADMIN_MENU:
                next_prompt = admin_prompt()

            elif next_prompt == PromptType.ADMIN_BOOK_ADD:
                add_book_prompt(book_service=self.book_service)
                next_prompt = PromptType.ADMIN_MENU

            elif next_prompt == PromptType.SEARCH_CATEGORY:
                search_by_category_prompt(book_service=self.book_service)
                next_prompt = PromptType.SEARCH_MENU
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