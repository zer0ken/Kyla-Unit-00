from langchain_core.tools import tool

from neo4j_db import query_neo4j


@tool
def query_db(query: str, description: str) -> str:
    """
    그래프 데이터베이스에서 질의를 실행합니다.
    질의는 Cypher statement의 형식을 지켜야 합니다.

    Args:
        query: Cypher statement.
        description: query가 무엇을 위한 것인지 설명하는 문자열.
    """
    if not query:
        return
    while '\\' in query:
        query = query.replace('\\', '')
    return {'description': description, 'result': query_neo4j(query)}


tools = [query_db]
