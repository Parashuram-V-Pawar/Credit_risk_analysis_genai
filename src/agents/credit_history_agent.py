from pydantic_ai import Agent

from src.agents.schemas import CreditHistoryAnalysis


credit_history_agent = Agent(
    "openai:gpt-5",
    output_type=CreditHistoryAnalysis,
    system_prompt="""
You are a credit bureau analyst.

Analyze:

- cibil score
- credit history
- previous loans
- default history

Provide historical credit assessment.
"""
)