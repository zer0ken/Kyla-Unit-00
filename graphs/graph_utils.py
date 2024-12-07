from langgraph.graph import StateGraph
from langchain_core.messages import AIMessageChunk


async def stream(graph: StateGraph, inputs: dict, config: dict = None) -> None:
    async for output_type, output in graph.astream(
        inputs,
        config=config,
        stream_mode=['updates', 'messages']
    ):
        if output_type == 'messages':
            chunk: AIMessageChunk = output[0]
            metadata: dict = output[1]
            print(chunk.content, flush=True, end='')
        elif output_type == 'updates':
            print('\n', flush=True)
            if 'chatbot' in output:
                output['chatbot']['messages'][-1].pretty_print()
            elif 'tools' in output:
                output['tools']['messages'][-1].pretty_print()
            print('\n', flush=True)
