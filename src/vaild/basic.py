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