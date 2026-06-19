from src.agents.llm_service import LLMService


class RiskAgent:

    def __init__(self):

        self.llm = LLMService()

    def analyze(
        self,
        default_probability,
        risk_level,
        customer_data,
        rag_context=None
    ):

        prompt = f"""
    You are a banking risk analyst.

    Facts:

    Default Probability:
    {default_probability:.4f}

    Risk Level:
    {risk_level}

    CIBIL:
    {customer_data['cibil_score']}

    Debt To Income Ratio:
    {customer_data.get("debt_to_income_ratio", 0)}

    Previous Loans:
    {customer_data['number_of_previous_loans']}

    Default History:
    {customer_data['default_history_count']}

    Rules:

    Only use supplied facts.
    No assumptions.
    Explain risk factors.
    Max 120 words.
    """

        return self.llm.generate(prompt)