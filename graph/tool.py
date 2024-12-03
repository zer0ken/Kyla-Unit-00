from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import ToolMessage
from langgraph.graph import END
from langgraph.prebuilt import ToolNode


def weather_tool(location: str) -> str:
    """
    특정 지역의 날씨를 알려주는 도구입니다.
    """
    return f'{location}의 날씨는 맑습니다.'

tool = TavilySearchResults(max_results=2)
tools = [tool, weather_tool]
tool_node = ToolNode(tools=tools)
