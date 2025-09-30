@echo off
REM 1) 콘솔 코드페이지를 UTF-8로
chcp 65001 >NUL

REM 2) 파이썬 I/O를 UTF-8로 강제
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8

REM 3) 가상환경 활성화
call .venv\Scripts\activate

REM 4) 실행 (cmd에서는 리다이렉션 사용 가능)
REM    표준출력은 UTF-8로 기록됨
python -X utf8 main.py < good.txt > output.txt

echo 실행이 완료되었습니다. output.txt 와 cli_app.log 파일을 확인하세요.
pause
