from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

class ContractChunker:
    """Handles text chunking for legal documents optimized for RAG."""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        # We use a recursive splitter tailored for standard legal paragraphs/sections
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ".", " ", ""]
        )
    
    def chunk_text(self, text: str, source: str = "contract") -> List[Document]:
        """Splits raw continuous text into smaller Documents for embeddings."""
        documents = self.splitter.create_documents(
            texts=[text], 
            metadatas=[{"source": source}]
        )
        return documents
