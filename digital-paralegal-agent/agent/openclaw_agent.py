from agent.skills.read_contract import execute_read_contract
from agent.skills.analyze_risk import execute_analyze_risk
from agent.skills.generate_report import execute_generate_report

class ContractAgent:
     """
     OpenClaw-style Agent Orchestrator.
     Defines the planner, executes sequential skills, and manages intermediate state.
     """
     
     def __init__(self):
         self.state = {}
         self.history = []
         
     def log_action(self, action: str, result: str):
         self.history.append({"action": action, "result": result})
         
     def run_workflow(self, file_bytes: bytes, filename: str) -> dict:
         """Executes the full agent pipeline synchronously for the contract."""
         
         # --- 1. Read & Index ---
         read_metadata = execute_read_contract(file_bytes, filename)
         self.log_action("read_contract", read_metadata.get("status", "failed"))
         
         if read_metadata.get("status") == "error":
             return {"error": read_metadata.get("message")}
             
         self.state["metadata"] = read_metadata
         
         # --- 2. Analyze Risks ---
         analysis = execute_analyze_risk()
         self.log_action("analyze_risk", f"Found {len(analysis)} risky clauses")
         self.state["analysis"] = analysis
         
         # --- 3. Generate Report ---
         report = execute_generate_report(self.state["analysis"], self.state["metadata"])
         self.log_action("generate_report", "Complete")
         
         # Append agent reasoning trace
         report["agent_trace"] = self.history
         
         return report
