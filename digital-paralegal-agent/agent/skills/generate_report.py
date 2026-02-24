from typing import List, Dict, Any

def calculate_risk_score(risks: List[Dict[str, Any]]) -> int:
    """Calculates an overall risk score from 0 to 100 based on findings."""
    score = 0
    weights = {
        "high": 30,
        "medium": 15,
        "low": 5,
        "none": 0
    }
    
    for risk in risks:
        level = risk.get("risk_level", "low").lower()
        score += weights.get(level, 0)
        
    return min(100, score) # Cap at 100

def execute_generate_report(analysis_results: List[Dict[str, Any]], read_metadata: dict) -> Dict[str, Any]:
    """
    Agent Skill: Aggregates the raw findings into a cohesive, structured JSON report suitable
    for a React frontend.
    """
    overall_score = calculate_risk_score(analysis_results)
    
    # Determine risk category
    if overall_score > 60:
         grade = "High Risk"
    elif overall_score > 30:
         grade = "Medium Risk"
    else:
         grade = "Low Risk"
         
    report = {
        "metadata": read_metadata,
        "executive_summary": {
            "overall_score": overall_score,
            "risk_grade": grade,
            "total_risks_found": len(analysis_results)
        },
        "identified_clauses": analysis_results
    }
    
    return report
