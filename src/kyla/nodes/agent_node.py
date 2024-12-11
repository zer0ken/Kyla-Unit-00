from datetime import datetime

from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage, AIMessage
from langchain_core.runnables import RunnableConfig
from langchain_google_genai import ChatGoogleGenerativeAI

from src.kyla.tools._screen import analyze_screenshot
from src.kyla.configuration import KylaConfiguration
from src.kyla.state import KylaState
from src.kyla.tools import global_llm_tools
from src.utils.llm_utils import default_param


class AgentNode:
    _llm = ChatGoogleGenerativeAI(**default_param)
    _llm = _llm.bind_tools(global_llm_tools)

    def __init__(self):
        self.llm = self._llm

    async def __call__(self, state: KylaState, config: RunnableConfig) -> KylaState:
        configurable = KylaConfiguration.from_runnable_config(config)
        updated_state = {}

        instruction = self.get_system_message(state, configurable)
    
        messages = state['messages']
        last_message = messages[-1]
        messages = messages[:-1]

        if state.get('plan_queue', []):
            messages.append(last_message)
            last_message = HumanMessage(content=self.get_task_instruction(state, configurable))
        elif type(last_message) is HumanMessage:
            last_message = HumanMessage(content=self.get_message_instruction(state, configurable))
        elif type(last_message) is ToolMessage and last_message.name == analyze_screenshot.name and last_message.content.startswith('data:image/png;base64,'):
            last_message = last_message.deepcopy()
            last_message.content = [
                {
                    'type': 'text',
                    'text': f'첨부된 이미지 파일({last_message.content})을 분석하세요.'
                },
                {
                    'type': 'image_url',
                    'image_url': last_message.content
                }
            ]
        elif type(last_message) is AIMessage and state.get('loop_count', 0):
            messages.append(last_message)
            last_message = HumanMessage(content=f'직전의 메시지에 대해 다시 깊이 생각해봐.')
        last_message.pretty_print()
        input_messages = [instruction] + messages + [last_message]

        response = await self.llm.ainvoke(input_messages)
        response.pretty_print()

        if state.get('loop_count', 0) > 0:
            updated_state['loop_count'] = state['loop_count'] - 1

        updated_state['messages'] = [response]
        return updated_state

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

    def get_message_instruction(self, state: KylaState, configurable: KylaConfiguration) -> str:
        return configurable.message_instruction.format(
            user=configurable.user_name,
            message=state['messages'][-1].content,
            background=state.get('query_results', '')
        )

    def get_after_tool_instruction(self, state: KylaState, configurable: KylaConfiguration) -> str:
        tool_results = []
        for message in state['messages'][::-1]:
            if type(message) is ToolMessage:
                tool_results.append(message.content)
            elif type(message) is HumanMessage:
                human_message = message.content
                break

        return configurable.after_tool_instruction.format(
            user=configurable.user_name,
            background=state.get('query_results', ''),
            message=human_message,
            tool_result=tool_results
        )
