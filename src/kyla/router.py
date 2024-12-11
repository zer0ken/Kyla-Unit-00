from typing import Literal
from langchain_core.messages import AIMessage
from langgraph.graph import END

from src.kyla.state import KylaState


def route_from_agent(state: KylaState) -> Literal['tools', 'end']:
    messages = state['messages']
    last_message = messages[-1]

    if isinstance(last_message, AIMessage):
        if tool_calls := last_message.tool_calls:
            return 'tools'

    return 'end'
