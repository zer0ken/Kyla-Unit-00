import os
import importlib
from langgraph.prebuilt import ToolNode

tools = []

for file in os.listdir(os.path.join(os.path.dirname(__file__), "_tools")):
    if not (not file.startswith("__") and file.startswith("_") and file.endswith(".py")):
        continue
    name = os.path.splitext(file)[0]
    module = importlib.import_module(f"graph._tools.{name}")
    tools.extend(module.tools)

tool_node = ToolNode(tools)
