from enum import Enum, auto

class PromptType(Enum):
    USER_MENU = auto()
    SEARCH_MENU = auto()
    ADMIN_MENU = auto()
    MAIN_MENU = auto()
    LOGIN = auto()
    BOOK_BORROW = auto()
    BOOK_RETURN = auto()
    SEARCH_BOOK = auto()
    SEARCH_CATEGORY = auto()
    LOGOUT = auto()