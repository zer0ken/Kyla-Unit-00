from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import tools_condition
from langgraph.checkpoint.memory import MemorySaver

from graph.state import State
from graph.nodes.llm import chatbot
from graph.tools import tool_node

graph_builder = StateGraph(State)

graph_builder.add_node('chatbot', chatbot)
graph_builder.add_node('tools', tool_node)

graph_builder.add_edge(START, 'chatbot')
graph_builder.add_edge('tools', 'chatbot')

graph_builder.add_conditional_edges('chatbot', tools_condition)

memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)


def stream_graph_updates(user_input: str, config: dict = None) -> None:
    events = graph.stream(
        {'messages': [('user', user_input)]},
        config=config, stream_mode='values'
    )
    for event in events:
        event['messages'][-1].pretty_print()
