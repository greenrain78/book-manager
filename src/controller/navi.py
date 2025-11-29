from src.controller.prompt import PromptType
from src.prompt.search import search_by_book_prompt, search_by_category_prompt
from src.prompt.user import user_prompt, search_prompt
from src.service.book_service import BookService


class NavigationController:
    def __init__(self, book_service: BookService):
        self.book_service = book_service

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