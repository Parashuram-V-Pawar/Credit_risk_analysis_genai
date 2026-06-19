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
        # LAZY MODELS
        # =========================
        self._approval_model = None
        self._default_model = None
        self._rag_engine = None

        # =========================
        # AGENTS
        # =========================
        self.approval_agent = ApprovalAgent()
        self.risk_agent = RiskAgent()
        self.coordinator_agent = CoordinatorAgent()
        self.history_agent = HistoryAgent()

        # =========================
        # CORE COMPONENTS
        # =========================
        self.risk_engine = RiskEngine()
        self.normalizer = DataNormalizer()

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
            try:
                self._rag_engine = RAGEngine()
            except Exception as e:
                print(f"RAG Initialization Failed: {e}")
                self._rag_engine = False
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
        # RAG RETRIEVAL
        # =========================
        rag_context = []
        policy_context = []

        rag = self.get_rag_engine()

        if rag:

            query = f"""
            CIBIL Score: {df['cibil_score'].iloc[0]}
            Annual Income: {df['annual_household_income'].iloc[0]}
            Loan Amount: {df['loan_amount'].iloc[0]}
            Defaults: {df['default_history_count'].iloc[0]}
            Previous Loans: {df['number_of_previous_loans'].iloc[0]}
            Debt Ratio: {df['debt_to_income_ratio'].iloc[0]}
            Risk Level: {risk_level}
            """

            try:
                rag_context = rag.retrieve(query)

                print("\nRAG RESULTS")
                print("=" * 50)

                for doc in rag_context:
                    print(doc[:200])

            except Exception as e:
                print("RAG ERROR:", e)

        # =========================
        # AGENTS
        # =========================
        approval_text = self.approval_agent.analyze(
            approval_prob,
            engineered_data,
            rag_context
        )

        risk_text = self.risk_agent.analyze(
            default_prob,
            risk_level,
            input_data,
            rag_context
        )

        history_analysis = self.history_agent.analyze(input_data)

        final_report = self.coordinator_agent.summarize(
            approval_text,
            risk_text,
            history_analysis,
            final_decision,
            rag_context
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

            "similar_cases": rag_context,

            "final_report": final_report
        }