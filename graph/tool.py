from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import ToolMessage
from langgraph.graph import END
from langgraph.prebuilt import ToolNode


tool = TavilySearchResults(max_results=2)
tools = [tool]
tool_node = ToolNode(tools=[tool])
