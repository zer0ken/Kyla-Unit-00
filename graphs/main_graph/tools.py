from langgraph.prebuilt import tools_condition

from global_tools.load_tools import load_tools
from graphs.main_graph.state import MainState


def get_available_tools() -> list:
    return load_tools("global_tools", "graphs.main_graph.local_tools")
