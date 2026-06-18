import joblib

class ModelLoader:

    def __init__(self):
        self._approval_model = None
        self._default_model = None

    def get_approval_model(self):
        if self._approval_model is None:
            import joblib
            self._approval_model = joblib.load("src/ml/models/loan_approval_model.pkl")
        return self._approval_model

    def get_default_model(self):
        if self._default_model is None:
            import joblib
            self._default_model = joblib.load("src/ml/models/default_risk_model.pkl")
        return self._default_model