from src.context import AppContext
from src.repository.entity import User
from src.repository.manager import BooksRepository, ISBNRepository, CategoryRepository, BorrowRepository, \
    UsersRepository


class UserService:
    def __init__(self, app: AppContext):
        self.users: UsersRepository = app.users_repo


    def can_signed_in(self) -> bool:
        # 20명 이하인 경우에만 회원가입 허용
        user_count = self.users.count_users()
        return user_count < 20

    def exist_user_id(self, user_id: str) -> bool:
        for u in self.users.data:
            if u.user_id == user_id:
                return True
        return False

    def add_user(self, user_id: str, pw: str, email: str) -> User:
        user = User(
            user_id=user_id,
            pw=pw,
            email=email,
        )
        self.users.insert(user)
        return user

    def get_user_by_id(self, user_id: str) -> User | None:
        for u in self.users.data:
            if u.user_id == user_id:
                return u
        return None