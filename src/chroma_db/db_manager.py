from uuid import uuid4
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

embeddings = HuggingFaceEmbeddings(
    model_name='src/chroma_db/ko-sroberta-multitask')


class ChromaDBManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.vector_store = Chroma(
            collection_name='kyla',
            embedding_function=embeddings,
            persist_directory='resources/chroma_db'
        )

    def add_documents(self, documents: list[Document]):
        documents_ = []
        uuids = []
        for document in documents:
            id_ = str(uuid4())
            document.metadata['id'] = id_
            uuids.append(id_)
            documents_.append(document)

        self.vector_store.add_documents(documents_, ids=uuids)

    def update_document(self, updated_documents: dict[str, tuple[str, dict]]):
        updated_uuids = []
        updated_documents_ = []

        for id_, document in updated_documents.items():
            page_content, metadata = document
            updated_uuids.append(id_)
            updated_documents_.append(Document(page_content=page_content, metadata=metadata, id=id_))

        self.vector_store.update_documents(
            ids=updated_uuids, documents=updated_documents_)

    def query(self, query: str, n_results: int = 10, filter: dict = None):
        return self.vector_store.similarity_search(query, k=n_results, filter=filter)
