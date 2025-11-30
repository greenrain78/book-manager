from logging import getLogger

from src.context import AppContext
from src.controller.prompt import PromptType
from src.prompt.admin import add_book_prompt
from src.prompt.menu import user_prompt, search_prompt, main_prompt, admin_prompt
from src.prompt.search import search_by_book_prompt, search_by_category_prompt
from src.prompt.start import login_prompt, signup_prompt

log = getLogger(__name__)


def handle_prompt(app: AppContext, prompt_type: PromptType) -> PromptType:
    """PromptType에 따른 흐름 처리를 수행하고 다음 PromptType을 반환한다."""

    if prompt_type == PromptType.USER_MENU:
        return user_prompt()

    elif prompt_type == PromptType.SEARCH_MENU:
        return search_prompt()

    elif prompt_type == PromptType.SEARCH_BOOK:
        search_by_book_prompt(book_service=app.book_service, borrow_service=app.borrow_service)
        return PromptType.SEARCH_MENU

    elif prompt_type == PromptType.MAIN_MENU:
        return main_prompt()

    elif prompt_type == PromptType.LOGIN:
        return login_prompt(user_service=app.user_service, app=app)

    elif prompt_type == PromptType.SIGNUP:
        return signup_prompt(user_service=app.user_service)

    elif prompt_type == PromptType.ADMIN_MENU:
        return admin_prompt()

    elif prompt_type == PromptType.ADMIN_BOOK_ADD:
        add_book_prompt(book_service=app.book_service)
        return PromptType.ADMIN_MENU

    elif prompt_type == PromptType.SEARCH_CATEGORY:
        search_by_category_prompt(book_service=app.book_service)
        return PromptType.SEARCH_MENU

    elif prompt_type == PromptType.EXIT:
        return PromptType.EXIT

    else:
        log.warning(f"Unknown prompt type: {prompt_type}")
        return PromptType.MAIN_MENU


def run_app_navigation(app: AppContext) -> None:
    """앱 내비게이션 루프를 시작한다."""
    next_prompt = PromptType.MAIN_MENU

    while next_prompt != PromptType.EXIT:
        next_prompt = handle_prompt(app, next_prompt)

    log.info("프로그램을 종료합니다.")