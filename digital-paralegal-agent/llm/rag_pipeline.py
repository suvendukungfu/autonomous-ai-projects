import os
from typing import List
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

class ContractRAG:
    """Manages the indexing and retrieval of contract embeddings using ChromaDB."""
    
    def __init__(self, persist_directory: str = None):
        if persist_directory is None:
            persist_directory = os.getenv("CHROMA_DB_DIR", "./chroma_db")
            
        self.embeddings = OpenAIEmbeddings()
        self.vector_store = Chroma(
            collection_name="contract_clauses",
            embedding_function=self.embeddings,
            persist_directory=persist_directory
        )
        
    def add_documents(self, documents: List[Document]):
        """Embeds and stores chunked document segments."""
        if documents:
            self.vector_store.add_documents(documents)
            
    def get_retriever(self, search_kwargs: dict = None):
        """Returns a configured retriever object."""
        if search_kwargs is None:
            search_kwargs = {"k": 10} # Bring back top 10 chunks per query by default
        return self.vector_store.as_retriever(search_kwargs=search_kwargs)

    def retrieve_context(self, query: str, top_k: int = 10) -> List[Document]:
        """Manually query for closest semantic match chunks against risk categories."""
        return self.vector_store.similarity_search(query, k=top_k)
