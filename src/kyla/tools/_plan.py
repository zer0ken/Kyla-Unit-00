from typing import Annotated
from langchain_core.tools import tool
from langgraph.prebuilt import InjectedState

from src.kyla.state import KylaState


@tool
def plan(goal: str, tasks: list[str]) -> dict:
    """
    계획 전문가처럼 복잡한 문제를 해결할 계획을 세우거나 수정합니다.
    계획을 세울 때는 목표를 최대한 작은 단계로 나누고, 각 단계에 활용하게 될 도구가 무엇일지 생각해보세요.
    도구가 필요 없는 단계는 하나로 합치세요.
    이 도구를 호출하고 나면 순차적으로 계획된 단계를 수행하게 됩니다.
    자신을 믿고 계획을 차근차근 수행해보세요.
    원하는 결과를 얻을 수 있을 겁니다.

    Args:
        goal: 달성하고자 하는 목표.
        tasks: 목표 달성을 위해 수행해야 하는 작업들의 리스트. 각 작업의 문자열에서 해당 단계에서 사용할 수 있는 도구들에 대해서도 언급하세요.
    """
    
    flatten = ''
    for task in tasks:
        flatten += f'- {task}\n'

    return f'"{goal}"를 달성하기 위해 다음의 계획을 세웠습니다.\n\n{flatten}'


tools = [plan]
