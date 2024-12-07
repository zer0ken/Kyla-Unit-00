from langgraph.prebuilt import ToolNode

from global_tools.load_tools import load_tools


def get_available_tools() -> list:
    return load_tools("tools") + load_tools("graphs.__template.local_tools")