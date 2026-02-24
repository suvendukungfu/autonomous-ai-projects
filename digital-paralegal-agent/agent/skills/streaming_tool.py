import os
from typing import AsyncGenerator
import json
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

class StreamingLLMTool:
    """Provides async generator capabilities for real-time UI streaming."""
    
    def __init__(self, model_name: str = "gpt-4o-mini", temperature: float = 0):
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            streaming=True
        )

    async def stream_structured_analysis(self, system_prompt: str, user_prompt: str) -> AsyncGenerator[str, None]:
        """Streams raw tokens back to the caller while parsing is handled on the client."""
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        
        async for chunk in self.llm.astream(messages):
            if chunk.content:
                # SSE format formatting
                yield f"data: {json.dumps({'token': chunk.content})}\n\n"
        yield "data: [DONE]\n\n"
