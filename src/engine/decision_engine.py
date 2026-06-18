class DecisionEngine:

    def decide(
        self,
        approval_probability,
        default_probability,
        risk_level,
        cibil_score,
        rag_context=None   # NEW (optional)
    ):

        reasons = []

        # 1. Hard rule (regulatory floor)
        if cibil_score < 550:
            return "REJECTED", ["CIBIL below minimum threshold"]

        # 2. Risk override
        if risk_level == "HIGH":
            reasons.append("High risk classification")

        # 3. ML signal
        if approval_probability > 0.60:
            reasons.append("Strong approval probability")
            decision = "APPROVED"
        else:
            decision = "MANUAL_REVIEW"

        # 4. Default risk adjustment
        if default_probability > 0.5:
            decision = "MANUAL_REVIEW"
            reasons.append("High default probability")

        # 5. RAG enhancement (NEW INTELLIGENCE)
        if rag_context:
            if "similar rejected cases" in rag_context.lower():
                reasons.append("Similar historical rejected cases found")

        # 6. Final override logic
        if risk_level == "HIGH" and approval_probability < 0.5:
            decision = "REJECTED"

        return decision, reasons