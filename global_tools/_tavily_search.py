from langchain_community.tools.tavily_search import TavilySearchResults

tools = [TavilySearchResults(
    max_results=3,
    description=f'tavily_search_results_json(query="the search query") - 웹 검색 엔진입니다. 웹 검색 결과 중 상위 {3}개를 json array 형식으로 반환합니다. 결과에는 각 검색한 웹 페이지의 url, 해당 페이지의 '
)]
