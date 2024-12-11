from dataclasses import field
from typing import Annotated, Optional
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage


class KylaState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    load_db_messages: Annotated[list[AnyMessage], add_messages]
    save_db_messages: Annotated[list[AnyMessage], add_messages]

    # Context states
    mood: Annotated[Optional[str], ...]
    user_mood: Annotated[Optional[str], ...]

    # DB states
    query_results: Annotated[list[dict], lambda l, r: l + r]
