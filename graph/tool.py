from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import ToolMessage
from langgraph.graph import END
import json

from graph.state import State


class BasicToolNode:
    def __init__(self, tools: list) -> None:
        self.tools_by_name = {tool.name: tool for tool in tools}

    def __call__(self, inputs: State) -> State:
        if messages := inputs.get('messages', []):
            messages = messages[-1]
        else:
            raise ValueError('No messages found in inputs')

        outputs = []
        for tool_call in messages.tool_calls:
            tool_result = self.tools_by_name[tool_call['name']].invoke(
                tool_call['args']
            )
            outputs.append(
                ToolMessage(
                    content=json.dumps(tool_result),
                    name=tool_call['name'],
                    tool_call_id=tool_call['id'],
                )
            )
        output = {'messages': outputs}
        print(f'... {output}')
        return output


tool = TavilySearchResults(max_results=2)
tools = [tool]

tool_node = BasicToolNode(tools=tools)

def route_tools(state: State) -> str:
    if isinstance(state, list):
        ai_message = state[-1]
    elif messages := state.get('messages', []):
        ai_message = messages[-1]
    else:
        raise ValueError(f'No messages found in state to route to tool_edge: {state}')
    
    if hasattr(ai_message, 'tool_calls') and len(ai_message.tool_calls) > 0:
        return 'tools'
    else:
        return END
