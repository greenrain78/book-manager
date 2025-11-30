from src.context import AppContext
from src.repository.entity import Borrow, BorrowHistory
from src.repository.manager import BorrowRepository


class BorrowService:
    def __init__(self, app: AppContext, navi = None):
        self.app = app
        self.borrow_repo: BorrowRepository = app.borrow_repo
        self.borrow_history_repo = app.borrow_history_repo

    # 대출중인지 확인
    def is_book_borrowed(self, book_id: str) -> bool:
        for borrow in self.borrow_repo.data:
            if borrow.book_id == book_id:
                return True
        return False

    # 반납하지 않은 책이 있는지 확인
    def has_unreturned_books(self) -> list:
        borrowed_books = []
        for borrow in self.borrow_repo.data:
            if borrow.user_id == self.app.current_user.user_id:
                borrowed_books.append(borrow.book_id)
        return borrowed_books

    def borrow_book(self, book_id: str) -> str:
        # 반납기한 계산
        due_date = (self.app.current_date + self.app.borrow_period).strftime("%Y-%m-%d")
        # 대출 처리
        self.borrow_repo.insert(Borrow(
            book_id=book_id,
            user_id=self.app.current_user.user_id,
            borrow_date=self.app.current_date.strftime("%Y-%m-%d"),
            due_date=due_date
        ))
        return due_date

    def return_book(self, borrow: Borrow) -> None:
        # 대출 내역에서 해당 도서 삭제
        self.borrow_repo.delete(book_id=borrow.book_id)
        self.borrow_history_repo.insert(BorrowHistory(
            book_id=borrow.book_id,
            user_id=borrow.user_id,
            borrow_date=borrow.borrow_date,
            due_date=borrow.due_date,
            return_date=self.app.current_date.strftime("%Y-%m-%d")
        ))