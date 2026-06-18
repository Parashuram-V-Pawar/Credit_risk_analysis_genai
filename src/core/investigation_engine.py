import joblib
import pandas as pd

from src.ml.feature_engineering import create_features
from src.agents.approval_agent import ApprovalAgent
from src.agents.risk_agent import RiskAgent
from src.agents.coordinator_agent import CoordinatorAgent
from src.agents.history_agent import HistoryAgent
from src.engine.risk_engine import RiskEngine
from src.core.data_normalizer import DataNormalizer


class CreditInvestigationEngine:

    def __init__(self):

        # ML Models
        self.approval_model = joblib.load(
            "src/ml/models/loan_approval_model.pkl"
        )

        self.default_model = joblib.load(
            "src/ml/models/default_risk_model.pkl"
        )

        # Agents
        self.approval_agent = ApprovalAgent()
        self.risk_agent = RiskAgent()
        self.coordinator_agent = CoordinatorAgent()
        self.history_agent = HistoryAgent()

        # Risk engine
        self.risk_engine = RiskEngine()

        # Normalizer
        self.normalizer = DataNormalizer()
        
        self.rag_engine = None   # attach later

    def evaluate_customer(self, input_data: dict):

        # =========================
        # NEW CUSTOMER HANDLING
        # =========================
        if input_data.get("is_new_customer", False):
            input_data.setdefault("cibil_score", 650)
            input_data.setdefault("credit_history", 0)
            input_data.setdefault("default_history_count", 0)
            input_data.setdefault("number_of_previous_loans", 0)

        # =========================
        # DATAFRAME CREATION
        # =========================
        data = self.normalizer.normalize(input_data)
        df = pd.DataFrame([data])

        # Feature Engineering
        df = create_features(df)

        engineered_data = df.iloc[0].to_dict()

        # =========================
        # ML PREDICTIONS
        # =========================
        approval_prob = self.approval_model.predict_proba(df)[0][1]
        default_prob = self.default_model.predict_proba(df)[0][1]

        approval = "APPROVED" if approval_prob > 0.5 else "REJECTED"

        # =========================
        # RISK ENGINE
        # =========================
        risk_result = self.risk_engine.calculate(
            cibil_score=float(df["cibil_score"].iloc[0]),
            default_probability=default_prob,
            debt_to_income_ratio=float(df["debt_to_income_ratio"].iloc[0])
        )

        risk_level = risk_result["risk_level"]
        risk_score = risk_result["risk_score"]

        # =========================
        # RAG (SAFE GUARD - OPTIONAL)
        # =========================
        rag_context = None
        policy_context = None

        if self.rag_engine:
            query_text = df.to_string()

            rag_context = self.rag_engine.retrieve_similar_cases(query_text)
            policy_context = self.rag_engine.get_policy_context(query_text)

        # =========================
        # FINAL DECISION LOGIC
        # =========================
        if approval == "REJECTED":
            final_decision = "REJECTED"

        elif risk_level == "HIGH":
            final_decision = "CONDITIONAL_APPROVAL"

        else:
            final_decision = "APPROVED"

        # =========================
        # AGENT ANALYSIS LAYER
        # =========================
        approval_text = self.approval_agent.analyze(
            approval_prob,
            engineered_data
        )

        risk_text = self.risk_agent.analyze(
            default_prob,
            risk_level,
            input_data
        )

        history_analysis = self.history_agent.analyze(input_data)

        final_report = self.coordinator_agent.summarize(
            approval_text,
            risk_text,
            history_analysis,
            final_decision
        )

        # =========================
        # RESPONSE
        # =========================
        return {
            "approval_probability": float(approval_prob),
            "default_probability": float(default_prob),

            "risk_score": risk_score,
            "risk_level": risk_level,

            "final_decision": final_decision,

            "approval_analysis": approval_text,
            "risk_analysis": risk_text,
            "history_analysis": history_analysis,
            "final_report": final_report,

            "rag_context": rag_context,
            "policy_context": policy_context
        }