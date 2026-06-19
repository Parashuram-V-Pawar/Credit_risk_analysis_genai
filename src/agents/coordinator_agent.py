from src.agents.llm_service import LLMService


class CoordinatorAgent:

    def __init__(self):
        self.llm = LLMService()

    def summarize(
        self,
        approval_analysis,
        risk_analysis,
        history_analysis,
        final_decision,
        rag_context=None
    ):

        rag_text = ""

        if rag_context:
            rag_text = "\n\nRelevant Historical Cases & Policies:\n"
            rag_text += "\n\n".join(rag_context)

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

        {rag_text}

        Instructions:
        - Use the historical cases and policy documents if relevant.
        - Compare the applicant against similar past cases.
        - Mention policy violations or policy strengths if found.
        - Explain whether the final decision aligns with previous cases.

        Provide:

        1. Executive Summary
        2. Strengths
        3. Risks
        4. Similar Historical Cases
        5. Policy Assessment
        6. Recommendation
        """

        return self.llm.generate(prompt)