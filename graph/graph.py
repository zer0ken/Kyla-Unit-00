from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import tools_condition

from graph.llm import chatbot
from graph.state import State
from graph.tool import tool_node

graph_builder = StateGraph(State)

graph_builder.add_node('chatbot', chatbot)
graph_builder.add_node('tools', tool_node)

graph_builder.add_edge(START, 'chatbot')
graph_builder.add_edge('tools', 'chatbot')

graph_builder.add_conditional_edges('chatbot', tools_condition)

graph = graph_builder.compile()


def stream_graph_updates(user_input: str) -> None:
    for event in graph.stream({'messages': [('user', user_input)]}):
        for value in event.values():
            print(f'Bot: {value['messages'][-1].content}')
