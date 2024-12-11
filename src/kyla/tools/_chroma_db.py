from langchain_core.tools import tool
from langchain.text_splitter import RecursiveCharacterTextSplitter

from src.chroma_db.db_manager import ChromaDBManager

db_manager = ChromaDBManager()
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=700, chunk_overlap=100
)


@tool
def memorize_information(information: str, source: str, timestamp: str):
    """
    정보를 오랫동안 자세히 기억하기 위해 이 도구를 사용하세요.
    이 도구는 요청을 받지 않더라도 원한다면 언제든지 스스로 판단하여 사용할 수 있습니다.
    입력된 정보는 데이터베이스에 저장되며 언제든지 다시 불러올 수 있습니다.

    Args:
        information: 기억할 정보. 길이에 제한이 없으므로 최대한 정확하고 상세하게 설명하는 것이 좋다. 한국어로 적는 것이 권장된다.
        source: 정보의 확실한 출처. 예를 들어, 웹 페이지의 URL이나 책의 제목 등을 인용하는 문자열이 될 수 있다. 대화를 통해 수집한 정보라면 정보를 제공한 사람의 이름을 적을 수 있다. 스스로 기록한 것이라면 자신의 이름을 적으면 된다.
        timestamp: 정보를 기억한 시간. 2024-01-01 12:00:00와 같은 형식으로 적을 것이 권장된다.
    """
    documents = text_splitter.create_documents(
        [information], metadatas=[{'source': source, 'timestamp': timestamp}])
    db_manager.add_documents(documents)

    flatten = ''
    for document in documents:
        flatten += f'- {document.page_content} (출처: {document.metadata["source"]}, 기억한 시간: {
            document.metadata["timestamp"]})\n'

    return f'정보가 데이터베이스에 저장되었습니다.\n\n{flatten}', documents


@tool
def recall_information(query: str):
    """
    정보를 정확히 떠올리기 위해 이 도구를 사용하세요.
    데이터베이스에서 관련된 정보를 찾아 불러옵니다.

    Args:
        query: 데이터베이스에서 찾을 정보와 관련성이 높은 단어나 문장. 한국어로 적는 것이 권장된다.
    """
    documents = db_manager.query(query, n_results=10)
    if not documents:
        return '데이터베이스에서 찾을 수 있는 정보가 없습니다.', []
    flatten = ''
    for document in documents:
        flatten += f'- {document.page_content} (출처: {document.metadata["source"]}, 기억한 시간: {
            document.metadata["timestamp"]})\n'
    return f'데이터베이스에서 찾은 정보입니다.\n\n{flatten}', documents


# tools = [memorize_information, recall_information]

tools = []
