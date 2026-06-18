from src.agents.llm_service import LLMService


class CoordinatorAgent:

    def __init__(self):
        self.llm = LLMService()

    def summarize(
        self,
        approval_analysis,
        risk_analysis,
        history_analysis,
        final_decision
    ):

        prompt = f"""
Create a professional credit investigation report.

Approval Analysis:
{approval_analysis}

Risk Analysis:
{risk_analysis}

Historical Analysis:
{history_analysis}

Final Decision:
{final_decision}

Provide:

1. Executive Summary
2. Strengths
3. Risks
4. Recommendation
"""

        return self.llm.generate(prompt)