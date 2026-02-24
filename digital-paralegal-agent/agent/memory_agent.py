from typing import List
from langchain_core.documents import Document
from llm.rag_pipeline import ContractRAG

class MemoryAgent:
    """Manages the agent's long-term memory of the contract context."""
    
    def __init__(self):
        self.rag = ContractRAG()
        
    def store_contract(self, documents: List[Document]):
        """Persist chunked document embeddings."""
        self.rag.add_documents(documents)
        return {"status": "success", "chunks_stored": len(documents)}
        
    def retrieve_context(self, query: str, top_k: int = 5) -> str:
        """Recall relevant semantic context for other agents."""
        docs = self.rag.retrieve_context(query, top_k=top_k)
        if not docs:
            return "No relevant context found in memory."
        return "\n\n---\n\n".join([d.page_content for d in docs])
