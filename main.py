from dotenv import load_dotenv

from graph.graph import graph, stream_graph_updates

if __name__ == '__main__':
    load_dotenv()
    
    graph.get_graph().print_ascii()
    
    while True:
        try:
            user_input = input('User: ')
            if user_input.lower() in ['exit', 'quit', 'q']:
                print('Goodbye!')
                break
            stream_graph_updates(user_input)
        except:
            user_input = 'LangGraph가 뭔지 설명해줘.'
            print(f'User: {user_input}')
            stream_graph_updates(user_input)
            break
