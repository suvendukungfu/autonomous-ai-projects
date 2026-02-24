from processing.parser import parse_document
from processing.chunker import ContractChunker
from llm.rag_pipeline import ContractRAG

def execute_read_contract(file_bytes: bytes, filename: str) -> dict:
    """
    Agent Skill: Reads a raw contract, chunks it, and loads it into the Vector DB.
    Returns metadata about the extracted document.
    """
    try:
        # 1. Parse into text
        raw_text = parse_document(file_bytes, filename)
        
        # 2. Chunk text
        chunker = ContractChunker()
        docs = chunker.chunk_text(raw_text, source=filename)
        
        # 3. Index to Vector DB
        rag = ContractRAG()
        rag.add_documents(docs)
        
        return {
            "status": "success",
            "message": f"Contract '{filename}' successfully read and indexed.",
            "total_chunks": len(docs),
            "doc_length": len(raw_text)
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to read contract: {str(e)}"
        }
