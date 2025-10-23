from src.repository.manager import UsersRepository, BooksRepository, BorrowHistoryRepository, BorrowRepository


class AppContext:
    def __init__(self):
        self.current_date = None
        self.current_user = None

        self.users = UsersRepository(path="data/users.txt")
        self.books = BooksRepository(path="data/books.txt")
        self.borrow = BorrowRepository(path="data/borrow.txt")
        self.borrow_history = BorrowHistoryRepository(path="data/borrow.txt")

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

    def set_current_user(self, user):
        self.current_user = user

    @staticmethod
    def exit_with_error(msg):
        print(msg)
        input("Press Enter to continue...") # 사용자에게 메시지를 읽을 시간을 줌
        raise SystemExit

