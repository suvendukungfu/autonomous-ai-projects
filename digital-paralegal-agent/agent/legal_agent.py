import json
from typing import Dict, Any, AsyncGenerator
from langchain_core.messages import SystemMessage, HumanMessage
from agent.skills.streaming_tool import StreamingLLMTool
from llm.prompts import RISK_PROMPT

class LegalAgent:
    """Specialized AI for analyzing specific legal clauses and streaming the resulting JSON."""
    
    def __init__(self):
        self.streamer = StreamingLLMTool(model_name="gpt-4o-mini", temperature=0)
        
    async def analyze_clause_stream(self, context: str, category: str) -> AsyncGenerator[str, None]:
        """Runs the analysis prompt and yields SSE formatted JSON tokens."""
        
        system_instruction = """
        You are an elite Digital Paralegal Agent AI.
        Your sole task is to analyze the provided contract context against specific legal risk categories.
        
        OUTPUT FORMAT MUST BE STRICT JSON NO MARKDOWN:
        {
          "clause_type": "string",
          "risk_level": "High | Medium | Low | None",
          "confidence_score": "0.0 to 1.0",
          "reasoning_steps": ["step 1", "step 2"],
          "explanation": "Final concise explanation"
        }
        """
        
        user_prompt = f"Analyze for category: {category}\n\nContext:\n{context}"
        
        async for chunk in self.streamer.stream_structured_analysis(system_instruction, user_prompt):
            yield chunk
