from enum import Enum, auto

class PromptType(Enum):
    MAIN_MENU = auto()
    USER_MENU = auto()
    SEARCH_MENU = auto()
    ADMIN_MENU = auto()
    CATEGORY_MENU = auto()


    LOGIN = auto()
    BOOK_BORROW = auto()
    BOOK_RETURN = auto()
    SEARCH_BOOK = auto()
    SEARCH_CATEGORY = auto()
    LOGOUT = auto()

    ADMIN_BOOK_MODIFY = auto()
    ADMIN_BOOK_DELETE = auto()
    ADMIN_BOOK_ADD = auto()