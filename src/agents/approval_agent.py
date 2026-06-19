from src.agents.llm_service import LLMService


class ApprovalAgent:

    def __init__(self):

        self.llm = LLMService()

    def analyze(
        self,
        approval_probability,
        customer_data,
        rag_context=None
    ):

        prompt = f"""
    You are a senior banking credit officer.

    Facts:

    Approval Probability:
    {approval_probability:.4f}

    CIBIL:
    {customer_data['cibil_score']}

    Annual Income:
    {customer_data['annual_household_income']}

    Loan Amount:
    {customer_data['loan_amount']}

    Debt To Income Ratio:
    {customer_data.get('debt_to_income_ratio', 'Calculated by system')}

    Rules:

    1. Use ONLY provided facts.
    2. Never invent data.
    3. Mention strengths.
    4. Mention concerns.
    5. Max 120 words.
    """

        return self.llm.generate(prompt)