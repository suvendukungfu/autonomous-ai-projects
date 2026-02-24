from typing import List, Dict, Any
import json
from langchain_openai import ChatOpenAI
from llm.prompts import RISK_PROMPT
from llm.rag_pipeline import ContractRAG

def execute_analyze_risk(risk_categories: List[str] = None) -> List[Dict[str, Any]]:
    """
    Agent Skill: Analyzes extracted contract chunks against common risk categories utilizing the RAG pipeline
    and the LLM prompt.
    """
    if risk_categories is None:
         risk_categories = ["indemnity", "termination clause", "liability limitation", "payment terms and penalties"]
         
    rag = ContractRAG()
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0) # Production reliability
    
    analysis_results = []
    
    for category in risk_categories:
        # Retrieve context for each category independently
        relevant_docs = rag.retrieve_context(category, top_k=5)
        
        # Aggregate text
        context_text = "\n\n".join([doc.page_content for doc in relevant_docs])
        
        if not context_text.strip():
             continue
             
        # Format prompt
        formatted_prompt = RISK_PROMPT.format(context=context_text)
        
        try:
             # Make the call
             response = llm.invoke(formatted_prompt)
             
             # The LLM is instructed to return raw JSON matching the schema.
             # Clean markdown wrappers if any exist
             content = response.content.strip()
             if content.startswith("```json"):
                 content = content[7:]
             if content.endswith("```"):
                 content = content[:-3]
                 
             result_json = json.loads(content.strip())
             result_json['searched_category'] = category
             
             # Only want real risks
             if result_json.get("risk_level", "None").lower() != "none":
                 analysis_results.append(result_json)
                 
        except Exception as e:
             # Silently skip format failures on individual shards
             print(f"Failed analysis for {category}: {e}")
             pass
    
    return analysis_results
