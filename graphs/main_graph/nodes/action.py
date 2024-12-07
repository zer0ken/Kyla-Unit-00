from langchain_core.tools import Tool
from langchain_core.messages import ToolMessage

from graphs.main_graph.state import MainState

class ActionNode:
    def __init__(self, tools: list[Tool]):
        self.tools_by_name = {tool.name: tool for tool in tools}
    
    def __call__(self, state: MainState) -> MainState:
        result = []
        for tool_call in state['messages'][-1].tool_calls:
            tool_name = tool_call['name']
            tool = self.tools_by_name[tool_name]
            observation = tool.invoke(tool_call["args"])
            tool_message = ToolMessage(content=observation, tool_call_id=tool_call["id"])
            tool_message.pretty_print()
            if tool_name == 'update_context':
                args = tool_call['args']
                return self._update_context(state, **args)
            result.append(tool_message)
        return {"messages": result}
    
    def _update_context(self, state: MainState, new_context: str) -> MainState:
        context_history = state['context_history'] + [state['context']]
        return {"context": new_context, "context_history": context_history} 
