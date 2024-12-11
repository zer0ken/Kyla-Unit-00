from datetime import datetime

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from langchain_google_genai import ChatGoogleGenerativeAI

from src.neo4j_db.neo4j_graph import get_neo4j_schema, refresh_neo4j_schema
from src.kyla.configuration import KylaConfiguration
from src.kyla.tools._neo4j_db import query_db
from src.kyla.state import KylaState
from src.utils.llm_utils import default_param


class SaveDBNode:
    _llm = ChatGoogleGenerativeAI(**default_param)
    _llm = _llm.bind_tools([query_db], tool_choice=query_db.name)

    def __call__(self, state: KylaState, config: RunnableConfig) -> KylaState:
        configurable = KylaConfiguration.from_runnable_config(config)

        last_message = state['messages'][-1]

        if type(last_message) is HumanMessage:
            last_message = HumanMessage(
                content=configurable.save_db_instruction.format(
                    schema=get_neo4j_schema(),
                    message=last_message.content,
                    user=configurable.user_name
                ),
                **last_message.additional_kwargs
            )
            last_message.pretty_print()
            response = self._llm.invoke(
                [self.get_system_message(state, configurable)]
                + [last_message]
            )
            refresh_neo4j_schema()
            return {'save_db_messages': [response]}

        return {'save_db_messages': []}

    def get_system_message(self, state: KylaState, configurable: KylaConfiguration) -> str:
        return SystemMessage(
            content=configurable.system_instruction.format(
                now=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                mood=state.get('mood', '불명'),
                topic=state.get('topic', '불명'),
                user=configurable.user_name,
                user_mood=state.get('user_mood', '불명')
            )
        )
