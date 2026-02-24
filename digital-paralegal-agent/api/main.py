from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from agent.planner_agent import PlannerAgent
from llm.rag_pipeline import ContractRAG

app = FastAPI(title="Advanced Multi-Agent Digital Paralegal API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze/stream")
async def analyze_document_stream(file: UploadFile = File(...)):
    """
    Kicks off the autonomous multi-agent planner loop and streams actions
    and clause reasoning back to the client via Server-Sent Events (SSE).
    """
    if not file.filename.lower().endswith(('.pdf', '.docx')):
         raise HTTPException(status_code=400, detail="Unsupported file format. Please upload PDF or DOCX.")
         
    file_bytes = await file.read()
    agent_brain = PlannerAgent()
    
    # Return a StreamingResponse utilizing the async generator from the Planner
    return StreamingResponse(
        agent_brain.run_autonomous_loop(file_bytes, file.filename),
        media_type="text/event-stream"
    )

@app.get("/memory/status")
async def memory_status():
    """Provides visibility into the Agent's ChromaDB RAG memory state."""
    rag = ContractRAG()
    try:
        # chroma collection row count
        count = rag.vector_store._collection.count()
        return {"status": "online", "chunks_in_memory": count}
    except Exception as e:
         return {"status": "error", "message": str(e)}
         
@app.get("/health")
async def health_check():
    return {"status": "ok", "agents_ready": True}

