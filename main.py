import logging

from src.context import AppContext
from src.prompt.start import date_input_prompt, main_prompt

logging.basicConfig(
    level=logging.DEBUG,                       # 로그 레벨 (DEBUG 이상 기록)
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",               # 시간 포맷
    handlers=[
        logging.FileHandler("debug.log", encoding="utf-8"),  # 파일 기록
    ]
)
log = logging.getLogger(__name__)

if __name__ == '__main__':
    log.debug(f"==================== 프로그램 시작 ====================")
    app = AppContext()
    # 날짜 입력
    date_input_prompt(app=app)
    # 메인 프롬프트
    main_prompt(app=app)
    log.debug(f"==================== 프로그램 종료 ====================")
