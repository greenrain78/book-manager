from src.context import AppContext
from src.screen import main_menu

if __name__ == '__main__':
    # 날짜 입력
    # 무결성 검사
    app = AppContext()
    main_menu(app=app)