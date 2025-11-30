from enum import Enum, auto

class PromptType(Enum):
    MAIN_MENU = auto()
    USER_MENU = auto()
    SEARCH_MENU = auto()
    ADMIN_MENU = auto()
    CATEGORY_MENU = auto()

    SIGNUP = auto()
    LOGIN = auto()
    EXIT = auto()

    CATEGORY_ASSIGN = auto()
    CATEGORY_MODIFY = auto()
    CATEGORY_MERGE = auto()
    CATEGORY_DELETE = auto()
    CATEGORY_ADD = auto()

    BOOK_BORROW = auto()
    BOOK_RETURN = auto()
    SEARCH_BOOK = auto()
    SEARCH_CATEGORY = auto()
    LOGOUT = auto()

    ADMIN_BOOK_MODIFY = auto()
    ADMIN_BOOK_DELETE = auto()
    ADMIN_BOOK_ADD = auto()