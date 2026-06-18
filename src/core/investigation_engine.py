import joblib
import pandas as pd

from src.ml.feature_engineering import create_features
from src.agents.approval_agent import ApprovalAgent
from src.agents.risk_agent import RiskAgent
from src.agents.coordinator_agent import CoordinatorAgent
from src.agents.history_agent import HistoryAgent
from src.engine.risk_engine import RiskEngine
from src.core.data_normalizer import DataNormalizer
from src.rag.rag_engine import RAGEngine


class CreditInvestigationEngine:

    def __init__(self):

        # =========================
        # LAZY MODELS (IMPORTANT FIX)
        # =========================
        self._approval_model = None
        self._default_model = None

        # Agents (safe lightweight objects)
        self.approval_agent = ApprovalAgent()
        self.risk_agent = RiskAgent()
        self.coordinator_agent = CoordinatorAgent()
        self.history_agent = HistoryAgent()

        # Core components
        self.risk_engine = RiskEngine()
        self.normalizer = DataNormalizer()

        # ⚠️ DO NOT INITIALIZE HEAVY RAG HERE
        self._rag_engine = None

    # =========================
    # MODEL LOADERS (LAZY)
    # =========================
    def get_approval_model(self):
        if self._approval_model is None:
            self._approval_model = joblib.load(
                "src/ml/models/loan_approval_model.pkl"
            )
        return self._approval_model

    def get_default_model(self):
        if self._default_model is None:
            self._default_model = joblib.load(
                "src/ml/models/default_risk_model.pkl"
            )
        return self._default_model

    def get_rag_engine(self):
        if self._rag_engine is None:
            self._rag_engine = RAGEngine()
        return self._rag_engine

    # =========================
    # MAIN ENGINE
    # =========================
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
        # NORMALIZE + DATAFRAME
        # =========================
        data = self.normalizer.normalize(input_data)
        df = pd.DataFrame([data])

        df = create_features(df)
        engineered_data = df.iloc[0].to_dict()

        # =========================
        # SAFE MODEL PREDICTIONS
        # =========================
        approval_model = self.get_approval_model()
        default_model = self.get_default_model()

        approval_prob = approval_model.predict_proba(df)[0][1]
        default_prob = default_model.predict_proba(df)[0][1]

        approval = "APPROVED" if approval_prob > 0.5 else "REJECTED"

        # =========================
        # RISK ENGINE
        # =========================
        risk_result = self.risk_engine.calculate(
            cibil_score=float(df["cibil_score"].iloc[0]),
            default_probability=float(default_prob),
            debt_to_income_ratio=float(df["debt_to_income_ratio"].iloc[0])
        )

        risk_level = risk_result["risk_level"]
        risk_score = risk_result["risk_score"]

        # =========================
        # RAG (SAFE LAZY LOAD)
        # =========================
        rag_engine = self.get_rag_engine()

        query_text = df.to_string()

        try:
            rag_context = rag_engine.retrieve_similar_cases(query_text)
            policy_context = rag_engine.get_policy_context(query_text)
        except Exception:
            rag_context = []
            policy_context = None

        # =========================
        # DECISION LOGIC
        # =========================
        if approval == "REJECTED":
            final_decision = "REJECTED"

        elif risk_level == "HIGH":
            final_decision = "CONDITIONAL_APPROVAL"

        else:
            final_decision = "APPROVED"

        # =========================
        # AGENTS
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
