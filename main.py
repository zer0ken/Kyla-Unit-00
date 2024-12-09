import asyncio
from IPython.display import Image
from dotenv import load_dotenv

from src.kyla.graph import MainGraphHolder


async def main():
    load_dotenv()

    graph_holder = MainGraphHolder()

    try:
        graph_img = Image(graph_holder.graph.get_graph().draw_mermaid_png())
        open('graph.png', 'wb').write(graph_img.data)
    except Exception as e:
        print(e)

    while True:
        try:
            user_input = input('\n>>> ')
            if user_input.lower() in ['exit', 'quit', 'q']:
                break
            if not user_input:
                continue
            await graph_holder.stream('제로켄', user_input)
        except Exception as e:
            print(e)
            break

if __name__ == '__main__':
    asyncio.run(main())
