from datetime import datetime

from langchain_core.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.text_splitter import RecursiveCharacterTextSplitter

from src.chroma_db.db_manager import ChromaDBManager

db_manager = ChromaDBManager()
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=700, chunk_overlap=100
)


tavily_search = TavilySearchResults(max_results=3, include_answer=True)

def get_timestamp():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

@tool
def search_web(query: str):
    """
    웹 검색 엔진입니다. 이 도구의 결과는 당신만 알 수 있습니다.
    검색 결과에는 각 검색한 웹 페이지의 URL, 해당 페이지에서 찾은 검색어와 관련된 내용을 포함합니다.
    검색 결과를 참고하여 추가적인 검색을 진행할 수도 있습니다.
    웹에서 검색하는 것이므로 결과가 정확하지 않을 수도 있습니다.

    Args:
        query: 검색어. 문장 혹은 단어일 수 있습니다.
    """
    results = tavily_search.invoke({'query': query})
    flatten = ''
    documents = []

    texts = []
    metadatas = []
    for result in results:
        text, url = result['content'], result['url']
        texts.append(text)
        metadatas.append({'source': url, 'timestamp': get_timestamp()})
        flatten += f'- {text} (출처: {url}, 기억한 시간: {get_timestamp()})\n'
    documents = text_splitter.create_documents(texts, metadatas)
    db_manager.add_documents(documents)
    print('검색 결과를 데이터베이스에 추가했습니다:', documents)
    return f'웹 검색 결과입니다.\n\n{flatten}', documents


tools = [search_web]
