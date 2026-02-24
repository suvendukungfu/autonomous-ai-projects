from langchain_core.prompts import PromptTemplate

RISK_ANALYSIS_PROMPT_TEMPLATE = """
As a Digital Paralegal AI, analyze the following contract excerpt for potential legal risks.
Focus specifically on detecting the following risk categories:
1. Indemnity
2. Termination
3. Liability
4. Payment Risk

Be precise and objective. If the clause heavily favors the other party, rank risk higher.
If the clause is standard or presents no particular risk, evaluate it as 'None'.

Contract Excerpt:
{context}

You must return your analysis EXCLUSIVELY as a JSON object matching the following schema.
Do not include any Markdown formatting, code blocks, or conversational text.

{{
  "clause_type": "Indemnity | Termination | Liability | Payment Risk | Other | None",
  "risk_level": "High | Medium | Low | None",
  "explanation": "Clear, concise reasoning justifying the risk level assigned. Summarize the risk dynamically."
}}
"""

RISK_PROMPT = PromptTemplate(
    template=RISK_ANALYSIS_PROMPT_TEMPLATE,
    input_variables=["context"]
)
