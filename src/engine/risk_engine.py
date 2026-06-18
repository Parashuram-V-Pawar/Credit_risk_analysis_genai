class RiskEngine:

    def __init__(self, rag_engine=None):
        self.rag = rag_engine

    # =========================
    # LEGACY (DO NOT REMOVE)
    # =========================
    def calculate(
        self,
        cibil_score,
        default_probability,
        debt_to_income_ratio
    ):

        risk_score = (
            (850 - cibil_score) * 0.4 +
            (default_probability * 100) * 0.4 +
            (debt_to_income_ratio * 100) * 0.2
        )

        if risk_score < 80:
            risk_level = "LOW"
        elif risk_score < 150:
            risk_level = "MEDIUM"
        else:
            risk_level = "HIGH"

        return {
            "risk_score": float(round(risk_score, 2)),
            "risk_level": risk_level
        }

    # =========================
    # NEW (RAG ENHANCED)
    # =========================
    def compute(
        self,
        cibil,
        dti,
        default_prob,
        customer_profile=None
    ):

        similar_cases = None

        if self.rag:
            query = f"CIBIL {cibil} DTI {dti} DEFAULT {default_prob}"
            similar_cases = self.rag.retrieve_similar_cases(query)

        risk_score = (
            (1 - cibil / 900) * 0.4 +
            dti * 0.3 +
            default_prob * 0.3
        )

        risk_level = (
            "HIGH" if risk_score > 0.7 else
            "MEDIUM" if risk_score > 0.4 else
            "LOW"
        )

        return {
            "risk_score": float(risk_score),
            "risk_level": risk_level,
            "similar_cases": similar_cases
        }

    # =========================
    # UNIFIED INTERFACE (IMPORTANT)
    # =========================
    def evaluate(
        self,
        cibil_score,
        default_probability,
        debt_to_income_ratio,
        customer_profile=None,
        use_rag=False
    ):

        if use_rag and self.rag:
            return self.compute(
                cibil_score,
                debt_to_income_ratio,
                default_probability,
                customer_profile
            )

        return self.calculate(
            cibil_score,
            default_probability,
            debt_to_income_ratio
        )