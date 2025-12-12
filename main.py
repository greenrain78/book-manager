import logging

from src.context import AppContext
from src.controller.navi import run_app_navigation
from src.prompt.start import date_input_prompt
from src.service.book_service import BookService
from src.service.borrow_service import BorrowService
from src.service.user_service import UserService

logging.basicConfig(
    level=logging.DEBUG,                       # 로그 레벨 (DEBUG 이상 기록)
    format="%(asctime)s [%(levelname)s] %(name)s:%(lineno)d - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",               # 시간 포맷
    handlers=[
        logging.FileHandler("debug.log", mode="w", encoding="utf-8"),  # 파일 기록
    ]
)
log = logging.getLogger(__name__)

if __name__ == '__main__':
    log.debug(f"==================== 프로그램 시작 ====================")
    app = AppContext()
    app.book_service = BookService(app=app)
    app.user_service = UserService(app=app)
    app.borrow_service = BorrowService(app=app)

    # 날짜 입력
    date_input_prompt(app=app)

    # 메인 프롬프트
    run_app_navigation(app=app)
    log.debug(f"==================== 프로그램 종료 ====================")
