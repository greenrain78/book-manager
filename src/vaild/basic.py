from datetime import datetime

from src.context import AppContext


def is_valid_date_format(date_str: str) -> bool:
    """Check if the date string is in YYYY-MM-DD format."""
    try:
        year, month, day = map(int, date_str.split('-'))
        if 1 <= month <= 12 and 1 <= day <= 31:
            return True
        else:
            return False
    except ValueError:
        return False

def is_previous_date(input_date) -> bool:
    """Check if the input date is before the current date."""
    #todo 현재 날짜와 비교하는 로직 추가
    return True

def valid_dates_on_start(app: AppContext) -> None:
    """
    Validate dates on application start.
    :param app:
    :return:
    """
    # if self.current_date is None:
    #     raise ValueError("현재 날짜가 설정되지 않았습니다.")

    all_dates = []

    # BorrowRepository
    for borrow in app.borrow.data:
        for date_str in [borrow.borrow_date, borrow.due_date]:
            try:
                all_dates.append(datetime.strptime(date_str, "%Y-%m-%d"))
            except Exception as e:
                raise e

    # BorrowHistoryRepository
    for history in app.borrow_history.data:
        for date_str in [history.borrow_date, history.due_date, history.return_date]:
            try:
                all_dates.append(datetime.strptime(date_str, "%Y-%m-%d"))
            except Exception as e:
                raise e

    # 모든 날짜가 현재 날짜보다 미래인지 확인
    if all_dates and all(date > app.current_date for date in all_dates):
        app.exit_with_error("모든 날짜가 현재 날짜보다 미래입니다. 날짜 데이터를 확인하세요.")