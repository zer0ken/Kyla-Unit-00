from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver


from graphs.graph_utils import stream
from graphs.main_graph.nodes.action import ActionNode
from graphs.main_graph.nodes.router import route_from_agent
from graphs.main_graph.state import MainState
from graphs.main_graph.tools import get_available_tools
from graphs.main_graph.nodes.agent import AgentNode

from prompts.load_prompt import load_prompt


class MainGraphHolder:
    DEFAULT_CONFIG = {"configurable": {"thread_id": "1"}}

    def __init__(self, config: dict = DEFAULT_CONFIG):
        self.config = config

        graph_builder = StateGraph(MainState)

        agent_node = AgentNode()
        graph_builder.add_node('agent', agent_node)

        action_node = ActionNode(get_available_tools())
        graph_builder.add_node('action', action_node)

        graph_builder.add_edge(START, 'agent')
        graph_builder.add_edge('action', 'agent')

        graph_builder.add_conditional_edges(
            'agent',
            route_from_agent,
            {
                'continue': 'action',
                'end': END
            }
        )

        memory = MemorySaver()
        self.graph = graph_builder.compile(checkpointer=memory)


        system_message = SystemMessage(content=load_prompt('system'))
        system_message.pretty_print()
        self.graph.update_state(
            self.config,
            {
                'instructions': [system_message],
                'context': '',
                'context_history': []
            }
        )

    async def stream(self, user_name: str, user_input: str) -> None:
        inputs = {'messages': [HumanMessage(content=f'{user_name}: {user_input}')]}
        await stream(self.graph, inputs, self.config)
