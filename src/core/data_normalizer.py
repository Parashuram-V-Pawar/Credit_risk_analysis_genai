class DataNormalizer:

    DEFAULTS = {
        "applicant_income": 0,
        "coapplicant_income": 0,
        "monthly_expense": 0,
        "existing_emis": 0,
        "asset_value": 0,
        "annual_household_income": 1,
    }

    def normalize(self, data: dict):

        for k, v in self.DEFAULTS.items():
            data.setdefault(k, v)

        return data