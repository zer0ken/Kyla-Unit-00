from langchain_community.tools.tavily_search import TavilySearchResults

MAX_RESULTS = 3

tools = [TavilySearchResults(
    max_results=MAX_RESULTS,
    include_answer=True,
    description='웹 검색 엔진입니다.\n'
                '결과에는 각 검색한 웹 페이지의 url, 해당 페이지에서 찾은 검색어와 관련된 내용을 포함합니다.\n'
                '웹에서 검색하는 것이므로 결과가 정확하지 않을 수도 있습니다.\n'
                'Args:\n'
                '    query: 검색어. 문장 혹은 단어일 수 있다.'
)]
