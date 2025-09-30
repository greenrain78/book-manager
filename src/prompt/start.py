from datetime import datetime

from src.context import AppContext
from src.prompt.common import clear_prompt
from src.vaild.basic import is_valid_date_format, is_previous_date


def date_input_prompt(app: AppContext) -> None:
    """
    날짜 입력 프롬프트
    :param app:
    :return:
    """
    clear_prompt()
    # 날짜 형식 무결성 검사
    while True:
        date_str = input("날짜를 입력하세요(YYYY-MM-DD): ").strip()
        # 날짜 형식 검사
        if not is_valid_date_format(date_str):
            print("잘못된 입력입니다!! 올바른 날짜를 입력하세요.")
            continue
        # 날짜 파싱
        try:
            now_date = datetime.strptime(date_str, "%Y-%m-%d")
        except Exception:
            print("잘못된 입력입니다!! 올바른 날짜를 입력하세요.")
            continue
        # 이전 날짜 검사
        if is_previous_date(now_date):
            print("이전 날짜를 입력했습니다!! 올바른 날짜를 입력하세요.")
            continue
        # 날짜 등록
        app.set_current_date(now_date)
        break
    return None


