from dotenv import load_dotenv

from graph.graph import MainGraph
load_dotenv()


if __name__ == '__main__':
    from IPython.display import Image
    try:
        graph_img = Image(graph.get_graph().draw_mermaid_png())
        open('graph.png', 'wb').write(graph_img.data)
    except Exception:
        pass

    graph = MainGraph()

    while True:
        try:
            user_input = input('\n>>> ')
            if user_input.lower() in ['exit', 'quit', 'q']:
                break
            if not user_input:
                continue
            graph.stream_graph_updates('제로켄', user_input)
        except:
            break
