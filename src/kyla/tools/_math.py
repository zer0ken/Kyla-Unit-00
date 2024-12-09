from typing import Tuple, Union
from langchain_core.tools import tool


@tool
def add(a: int, b: int) -> int:
    """
    두 수를 더합니다.

    Args:
        a: 첫 번째 수
        b: 두 번째 수
    """
    return a + b


@tool
def sub(a: int, b: int) -> int:
    """
    첫 번째 수에서 두 번째 수를 뺍니다.

    Args:
        a: 첫 번째 수
        b: 두 번째 수
    """
    return a - b


@tool
def mul(a: int, b: int) -> int:
    """
    첫 번째 수에 두 번째 수를 곱합니다.

    Args:
        a: 첫 번째 수
        b: 두 번째 수
    """
    return a * b


@tool
def div(a: int, b: int, div_and_mod: bool = False) -> Union[int, Tuple[int, int]]:
    """
    첫 번째 수를 두 번째 수로 나눕니다.

    Args:
        a: 첫 번째 수
        b: 두 번째 수
        div_and_mod: 몫과 나머지를 동시에 반환할지 여부. 기본값은 False.
    """
    if div_and_mod:
        return a // b, a % b
    return a / b


@tool
def pow(a: int, b: int) -> int:
    """
    첫 번째 수를 두 번째 수만큼 거듭제곱합니다.

    Args:
        a: 첫 번째 수
        b: 두 번째 수
    """
    return a ** b


@tool
def round(a: float) -> int:
    """
    소수점을 반올림합니다.
    """
    return round(a)


tools = [add, sub, mul, div, pow, round]
