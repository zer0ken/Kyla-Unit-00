from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from src.kyla.nodes import (
    AgentNode,
    ToolNode,
    LoadDBNode,
    SaveDBNode
)
from src.kyla.router import (
    route_from_agent
)
from src.kyla.configuration import KylaConfiguration
from src.kyla.state import KylaState
from src.kyla.tools import global_llm_tools
from src.kyla.tools._neo4j_db import query_db


builder = StateGraph(state_schema=KylaState, config_schema=KylaConfiguration)

""" Nodes """

load_db_node = LoadDBNode()
builder.add_node('load_db', load_db_node)

load_db_tool_node = ToolNode([query_db], message_path='load_db_messages')
builder.add_node('load_db_tool', load_db_tool_node)

save_db_node = SaveDBNode()
builder.add_node('save_db', save_db_node)

save_db_tool_node = ToolNode([query_db], message_path='save_db_messages')
builder.add_node('save_db_tool', save_db_tool_node)

agent_node = AgentNode()
builder.add_node('agent', agent_node)

agent_tool_node = ToolNode(global_llm_tools)
builder.add_node('agent_tool', agent_tool_node)

""" Edges """

builder.add_edge(START, 'load_db')
builder.add_edge('load_db', 'load_db_tool')
builder.add_edge('load_db_tool', 'agent')

builder.add_edge(START, 'save_db')
builder.add_edge('save_db', 'save_db_tool')
builder.add_edge('save_db_tool', 'agent')

builder.add_edge('agent_tool', 'agent')

builder.add_conditional_edges(
    'agent',
    route_from_agent,
    {
        'tools': 'agent_tool',
        'end': END
    }
)

memory = MemorySaver()
graph = builder.compile(checkpointer=memory)
