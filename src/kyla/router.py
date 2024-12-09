from langchain_core.messages import AIMessage
from langgraph.graph import END

from src.kyla.state import MainState


def route_from_agent(state: MainState) -> str:
    messages = state['messages']
    last_message = messages[-1]

    if isinstance(last_message, AIMessage):
        if last_message.tool_calls:
            return 'tools'
    return 'end'