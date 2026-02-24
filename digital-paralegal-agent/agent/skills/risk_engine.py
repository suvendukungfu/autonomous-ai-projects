from typing import Dict, Any

def execute_risk_scoring(clause_analysis: Dict[str, Any]) -> int:
    """
    Rule-based Risk Engine.
    Assigns numerical severity based on category and LLM-defined risk level.
    """
    level = clause_analysis.get("risk_level", "None").lower()
    
    weights = {
        "high": 35,
        "medium": 15,
        "low": 5,
        "none": 0
    }
    
    base_score = weights.get(level, 0)
    
    # Optional multipliers based on specific clause types
    clause_type = clause_analysis.get("clause_type", "").lower()
    if "indemnity" in clause_type and level == "high":
        base_score += 15 # Severe penalty for high-risk indemnity
        
    return base_score
