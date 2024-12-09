def get_available_tools() -> list:
    from src.utils.tool_utils import load_tools
    return load_tools("src.kyla.tools")
