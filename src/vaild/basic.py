import re
from datetime import datetime

from src.context import AppContext


def is_valid_date_format(date_str: str) -> bool:
    """Check if the date string is in YYYY-MM-DD format."""
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date_str):
        return False
    try:
        year, month, day = map(int, date_str.split('-'))
        if 1 <= month <= 12 and 1 <= day <= 31:
            return True
        else:
            return False
    except ValueError:
        return False

    # if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", v):


def is_previous_date(input_date: datetime, app: AppContext) -> bool:
    """Check if the input date is before the current date."""
    all_dates = []

    # BorrowRepository
    for borrow in app.borrow_repo.data:
        for date_str in [borrow.borrow_date]:
            try:
                all_dates.append(datetime.strptime(date_str, "%Y-%m-%d"))
            except Exception as e:
                raise e

    # BorrowHistoryRepository
    for history in app.borrow_history_repo.data:
        for date_str in [history.borrow_date, history.return_date]:
            try:
                all_dates.append(datetime.strptime(date_str, "%Y-%m-%d"))
            except Exception as e:
                raise e
    if all_dates and any(date > input_date for date in all_dates):
        return False
    return True
