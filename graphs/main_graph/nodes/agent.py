from graphs.llm_generator import generate_llm
from graphs.main_graph.state import MainState
from graphs.main_graph.tools import get_available_tools
from prompts.load_prompt import load_prompt

class AgentNode:
    SYSTEM_INSTRUCTION = load_prompt('system')

    def __init__(self):
        self.llm = generate_llm()
        self.llm = self.llm.bind_tools(get_available_tools())
    
    async def __call__(self, state: MainState) -> MainState:
        messages = state['messages']
        instructions = state['instructions']
        response = await self.llm.ainvoke(instructions + messages)
        response.pretty_print()
        updated_state = {'messages': [response]}
        return updated_state

    def get_system_message(self, state: MainState):
        return self.SYSTEM_INSTRUCTION.format(context=state['context'])

