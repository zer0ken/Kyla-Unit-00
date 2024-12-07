from langchain_core.tools import tool


@tool
def tool_name(args) -> str:
    """
    docstring을 작성해야 합니다.
    """
    return {'result': 'dict 타입으로 반환하는 것이 정신 건강에 이롭습니다.'}


tools = [tool_name]
