import joblib


class ModelLoader:

    def __init__(self):

        self.approval_model = joblib.load(
            "src/ml/models/loan_approval_model.pkl"
        )

        self.default_model = joblib.load(
            "src/ml/models/default_risk_model.pkl"
        )

    def get_approval_model(self):
        return self.approval_model

    def get_default_model(self):
        return self.default_model