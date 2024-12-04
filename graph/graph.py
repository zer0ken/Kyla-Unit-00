from langgraph.graph import StateGraph, START
from langgraph.prebuilt import tools_condition
from langgraph.checkpoint.memory import MemorySaver

from graph.state import State
from graph.nodes.logical_llm import logical_llm_node
from graph.tools import tool_node
from prompt.load import load_prompt

class MainGraph:
    def __init__(self):
        self.config = {"configurable": {"thread_id": "1"}}

        graph_builder = StateGraph(State)

        graph_builder.add_node('chatbot', logical_llm_node)
        graph_builder.add_node('tools', tool_node)

        graph_builder.add_edge(START, 'chatbot')
        graph_builder.add_edge('tools', 'chatbot')

        graph_builder.add_conditional_edges('chatbot', tools_condition)

        memory = MemorySaver()
        self.graph = graph_builder.compile(checkpointer=memory)
    
        self.graph.update_state(self.config, {"messages": [("system", load_prompt('persona'))]})

    def stream_graph_updates(self, user_name: str, user_input: str) -> None:
        events = self.graph.stream(
            {'messages': [('user', f'{user_name}의 발언: {user_input}')]},
            config=self.config, stream_mode='values'
        )
        for event in events:
            event['messages'][-1].pretty_print()
