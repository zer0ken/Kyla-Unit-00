def get_available_tools() -> list:
    from utils.tool_utils import load_tools
    return load_tools("kyla.utils.tools")
