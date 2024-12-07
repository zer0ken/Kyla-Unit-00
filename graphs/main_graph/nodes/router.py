from langchain_core.messages import AIMessage
from langgraph.graph import END

from graphs.main_graph.state import MainState


def route_from_agent(state: MainState) -> str:
    messages = state['messages']
    last_message = messages[-1]

    if isinstance(last_message, AIMessage) and last_message.tool_calls:
        return 'continue'
    return 'end'