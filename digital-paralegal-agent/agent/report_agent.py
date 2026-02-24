from typing import List, Dict, Any
from agent.skills.risk_engine import execute_risk_scoring

class ReportAgent:
    """Agent responsible for compiling final structured outputs and metadata."""
    
    def __init__(self):
        pass
        
    def compile_final_report(self, agent_trace: List[Dict[str, Any]], clause_results: List[Dict[str, Any]], metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Aggregate all memory and execution traces into a master JSON blob."""
        
        # Calculate aggregate
        total_score = sum(execute_risk_scoring(c) for c in clause_results)
        
        if total_score > 50:
             grade = "Critical Risk"
        elif total_score > 20:
             grade = "Moderate Risk"
        else:
             grade = "Low Risk"
             
        # Filter raw none
        actual_risks = [c for c in clause_results if c.get("risk_level", "none").lower() != "none"]
        
        report = {
            "metadata": metadata,
            "executive_summary": {
                "overall_risk_score": min(total_score, 100),
                "risk_grade": grade,
                "total_clauses_flagged": len(actual_risks)
            },
            "clause_analysis": actual_risks,
            "autonomous_reasoning_trace": agent_trace
        }
        return report
