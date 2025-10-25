from logging import getLogger
from typing import Callable, Any

log = getLogger(__name__)


def input_with_validation(
    prompt: str,
    validators: list[tuple[Callable[[str], bool], str]],
    retry: bool = True
) -> str | None:
    """
    입력을 받고 여러 검증 함수를 적용.
    - validators: [(검증함수, 실패시 메시지), ...]
    - 모든 검증을 통과하면 입력값 반환
    """
    while True:
        value = input(prompt)
        log.debug(f"{prompt}:: {value}")
        valid = True
        for fn, msg in validators:
            if not fn(value):
                print(msg)
                valid = False
                break
        if valid:
            return value
        if not retry:
            return None

def parse_with_validation(
    value: str,
    parse_fn: Callable[[str], Any],
    parse_err_msg: str,
    validators: list[tuple[Callable[[Any], bool], str]],
    retry: bool = True
) -> Any | None:
    """
    입력값을 받고 여러 파싱 함수를 적용.
    - parsers: [(파싱함수, 실패시 메시지), ...]
    - 모든 파싱을 통과하면 파싱된 값 반환
    """
    while True:
        try:
            value = parse_fn(value)
        except Exception:
            print(parse_err_msg)
            return None
        log.debug(f"parse_with_validation:: {value}")
        valid = True
        for fn, msg in validators:
            if not fn(value):
                print(msg)
                valid = False
                break
        if valid:
            return value
        if not retry:
            return None