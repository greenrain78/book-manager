from datetime import datetime, timedelta

from src.context import AppContext
from src.repository.entity import Borrow, BorrowHistory
from src.repository.manager import BorrowRepository


class BorrowService:
    def __init__(self, app: AppContext, navi = None):
        self.app = app
        self.borrow_repo: BorrowRepository = app.borrow_repo
        self.borrow_history_repo = app.borrow_history_repo
        self.users_repo = app.users_repo

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
                borrowed_books.append(borrow)
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
        due_date = datetime.strptime(borrow.due_date, "%Y-%m-%d")
        if self.app.current_date > due_date:
            overdue_days = (self.app.current_date - due_date).days
            user = self.users_repo.find_by_id(borrow.user_id)
            if not user:
                raise self.app.exit_with_error("사용자 정보를 찾을 수 없습니다.")
            current_penalty_date = datetime.strptime(user.penaltyDate, "%Y-%m-%d") if user.penaltyDate else self.app.current_date
            new_penalty_start = max(self.app.current_date, current_penalty_date)
            new_penalty_date = new_penalty_start + timedelta(days=overdue_days)
            user.penaltyDate = new_penalty_date.strftime("%Y-%m-%d")
            self.users_repo.modify(
                user_id=user.user_id,
                new_penaltyDate=user.penaltyDate
            )
            print(f"책이 연체되었습니다. 제재 기간은 {user.penaltyDate}입니다.")

        # 대출 내역에서 해당 도서 삭제
        self.borrow_repo.delete(book_id=borrow.book_id)
        self.borrow_history_repo.insert(BorrowHistory(
            book_id=borrow.book_id,
            user_id=borrow.user_id,
            borrow_date=borrow.borrow_date,
            due_date=borrow.due_date,
            return_date=self.app.current_date.strftime("%Y-%m-%d")
        ))


    # 해당 사용자의 패널티 날짜 조회
    def get_user_penalty_date(self) -> datetime:
        # 현재 사용자 정보 조회
        user = self.users_repo.find_by_id(self.app.current_user.user_id)
        if not user:
            raise self.app.exit_with_error("사용자 정보를 찾을 수 없습니다.")
        return datetime.strptime(user.penaltyDate, "%Y-%m-%d") if user.penaltyDate else None