from typing import AsyncGenerator, Dict, Any, List
import json
import asyncio
from processing.parser import parse_document
from processing.chunker import ContractChunker
from agent.memory_agent import MemoryAgent
from agent.legal_agent import LegalAgent
from agent.report_agent import ReportAgent

class PlannerAgent:
    """
    The main autonomous brain of the digital paralegal system.
    Evaluates state, coordinates Memory/Legal/Report agents, and yields
    streaming trace events followed by JSON tokens to the frontend.
    """
    
    def __init__(self):
        self.memory = MemoryAgent()
        self.legal_agent = LegalAgent()
        self.report_agent = ReportAgent()
        self.trace_log: List[Dict[str, str]] = []
        self.analysis_results: List[Dict[str, Any]] = []
        
    def _log_trace(self, agent: str, action: str, result: str):
        self.trace_log.append({
            "agent": agent,
            "action": action,
            "result": result
        })
        
    async def _yield_trace_event(self, agent: str, action: str, result: str) -> str:
        """Helper to format SSE reasoning events for real-time UI updates."""
        self._log_trace(agent, action, result)
        trace_data = {
            "type": "trace",
            "agent": agent,
            "action": action,
            "result": result
        }
        return f"data: {json.dumps(trace_data)}\n\n"
        
    async def run_autonomous_loop(self, file_bytes: bytes, filename: str) -> AsyncGenerator[str, None]:
        """
        The core OpenClaw autonomous loop: Observe -> Plan -> Act -> Reflect
        Yields Server-Sent Events (SSE) representing state changes and streaming LLM tokens.
        """
        
        # --- 1. OBSERVE / SETUP ---
        yield await self._yield_trace_event("Planner", "Initialize", f"Starting workflow for document: {filename}")
        
        try:
             # Tool Usage: Extract Text
             yield await self._yield_trace_event("ParserTool", "Extract", "Parsing raw text from document bytes.")
             raw_text = parse_document(file_bytes, filename)
             
             yield await self._yield_trace_event("ChunkerTool", "Split", "Chunking text into semantic segments for RAG.")
             chunker = ContractChunker()
             docs = chunker.chunk_text(raw_text, source=filename)
             doc_metadata = {"filename": filename, "total_chunks": len(docs), "total_chars": len(raw_text)}
             
             # Agent Action: Store to Memory
             yield await self._yield_trace_event("MemoryAgent", "Store", f"Indexing {len(docs)} chunks into Vector DB.")
             self.memory.store_contract(docs)
             
        except Exception as e:
             yield await self._yield_trace_event("System", "Error", f"Failed Processing: {str(e)}")
             yield "data: [DONE]\n\n"
             return
             
        # --- 2. PLAN ---
        risk_categories = ["Indemnity Clauses", "Termination Conditions", "Liability Limitations", "Payment Risks"]
        yield await self._yield_trace_event("Planner", "Plan", f"Scheduled sequential analysis for {len(risk_categories)} risk vectors.")
        
        # --- 3. ACT & REFLECT (Autonomous Loop) ---
        for category in risk_categories:
            yield await self._yield_trace_event("Planner", "Execute", f"Retrieving legal precedent and context for: {category}")
            
            # Agent Action: Retrieve Memory
            context = self.memory.retrieve_context(category, top_k=6)
            
            if "No relevant context" in context:
                yield await self._yield_trace_event("Planner", "Reflect", f"Skipping {category}: No relevant text found in document.")
                continue
                
            yield await self._yield_trace_event("LegalAgent", "Analyze", f"Analyzing {category} context via LLM stream...")
            
            # Start streaming analysis specific to this clause
            # We yield a special wrapper event to tell the UI an LLM stream is starting
            start_event = {"type": "stream_start", "category": category}
            yield f"data: {json.dumps(start_event)}\n\n"
            
            buffer = ""
            async for chunk in self.legal_agent.analyze_clause_stream(context, category):
                 # Pass through raw LLM SSE stream directly to client
                 yield chunk
                 
                 # accumulate buffer for final report agent aggregation
                 # The chunk format is `data: {"token": "..."}\n\n`
                 if chunk.startswith("data: {"):
                      try:
                          payload = json.loads(chunk[6:])
                          if "token" in payload:
                              buffer += payload["token"]
                      except json.JSONDecodeError:
                          pass
                          
            # End sequence for this specific category UI block
            end_event = {"type": "stream_end", "category": category}
            yield f"data: {json.dumps(end_event)}\n\n"
            
            # Reflect: Attempt to parse the completed buffer
            try:
                # The LLM prompt forces strict JSON, but it might get wrapped in markdown
                clean_buffer = buffer.strip()
                if clean_buffer.startswith("```json"):
                     clean_buffer = clean_buffer[7:]
                if clean_buffer.endswith("```"):
                     clean_buffer = clean_buffer[:-3]
                     
                result_json = json.loads(clean_buffer.strip())
                result_json["category"] = category
                self.analysis_results.append(result_json)
                yield await self._yield_trace_event("Planner", "Reflect", f"Successfully captured findings for {category}.")
            except Exception as e:
                yield await self._yield_trace_event("Planner", "Reflect", f"Failed to parse LLM structured output for {category}.")
                
        # --- 4. FINALIZE ---
        yield await self._yield_trace_event("ReportAgent", "Compile", "Aggregating all agent outputs into final structured report.")
        final_report = self.report_agent.compile_final_report(self.trace_log, self.analysis_results, doc_metadata)
        
        report_event = {
            "type": "final_report",
            "report": final_report
        }
        yield f"data: {json.dumps(report_event)}\n\n"
        
        # Conclude SSE Connection
        yield "data: [DONE]\n\n"
