from langchain_core.tools import Tool
from langchain_core.messages import ToolMessage, AIMessage

from src.kyla.state import MainState


class ActionNode:
    def __init__(self, tools: list[Tool]):
        self.tools_by_name = {tool.name: tool for tool in tools}

    def __call__(self, state: MainState) -> MainState:
        results = []
        for tool_call in state['messages'][-1].tool_calls:
            tool_name = tool_call['name']
            tool = self.tools_by_name[tool_name]
            observation = tool.invoke(tool_call["args"])
            tool_message = ToolMessage(
                content=observation,
                tool_call_id=tool_call["id"],
                name=tool_name
            )
            tool_message.pretty_print()

            # add additional task here

            results.append(tool_message)

        print(results)
        return {"messages": results}
