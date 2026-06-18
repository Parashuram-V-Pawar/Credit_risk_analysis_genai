from src.agents.llm_service import LLMService


class HistoryAgent:

    def __init__(self):
        self.llm = LLMService()

    def analyze(self, customer_data):

        prompt = f"""
Analyze customer borrowing history.

Facts:

Previous Loans:
{customer_data['number_of_previous_loans']}

Default History:
{customer_data['default_history_count']}

Credit History Length:
{customer_data['credit_history']}

Rules:

Use ONLY supplied facts.
Do not assume anything.
Do not invent information.

Provide:
1. Repayment Behaviour
2. Borrowing Experience
3. Credit Discipline
"""

        return self.llm.generate(prompt)