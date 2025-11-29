from src.prompt.search import search_by_book_prompt
from src.service.book_service import BookService


class MainController:
    def __init__(self):
        pass

    def book_search(self):
        pass

    def book_borrow(self):
        pass
    def book_return(self):
        pass
    def user_logout(self):
        pass

class SearchController:
    def __init__(self, app):
        self.book_service = BookService(app)

    def search(self):
        search_by_book_prompt(service=self.book_service)

    def search_by_category(self):
        pass