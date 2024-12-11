from langchain_core.messages import ToolMessage
from langchain_core.runnables import RunnableConfig

from src.kyla.tools._neo4j_db import query_db
from src.kyla.state import KylaState


class ToolNode:
    def __init__(self, tools: list, message_path: str = 'messages'):
        self.tools_by_name = {tool.name: tool for tool in tools}
        self.message_path = message_path

    def __call__(self, state: KylaState, config: RunnableConfig) -> KylaState:
        updated_state = {}

        messages = []
        for tool_call in state[self.message_path][-1].tool_calls:
            tool_name = tool_call['name']
            tool = self.tools_by_name[tool_name]
            observation = tool.invoke(tool_call["args"])
            tool_message = ToolMessage(
                content=observation,
                tool_call_id=tool_call["id"],
                name=tool_name
            )

            """add additional task below"""
            
            if tool_name == query_db.name and observation:
                updated_state['query_results'] = [observation]

            """add additional task above"""

            messages.append(tool_message)

        updated_state[self.message_path] = messages

        print('@@@@ tool node @@@@', updated_state)
        return updated_state
