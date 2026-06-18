import pandas as pd


class FeatureBuilder:

    def build(self, customer: dict, loan_request: dict):

        data = {}

        # =========================
        # CUSTOMER PROFILE
        # =========================
        data["age"] = customer.get("age")
        data["gender"] = customer.get("gender")
        data["married"] = customer.get("married")
        data["education"] = customer.get("education")
        data["occupation"] = customer.get("occupation")

        # =========================
        # EMPLOYMENT
        # =========================
        data["employment_status"] = customer.get("employment_status")
        data["employment_length_years"] = customer.get(
            "employment_length_years"
        )
        data["business_type"] = customer.get("business_type")
        data["organization_type"] = customer.get(
            "organization_type"
        )

        # =========================
        # FINANCIAL
        # =========================
        data["applicant_income"] = customer.get(
            "applicant_income",
            0
        )

        data["coapplicant_income"] = customer.get(
            "coapplicant_income",
            0
        )

        data["annual_household_income"] = customer.get(
            "annual_household_income",
            0
        )

        data["monthly_expense"] = customer.get(
            "monthly_expense",
            0
        )

        data["asset_value"] = customer.get(
            "asset_value",
            0
        )

        data["existing_emis"] = customer.get(
            "existing_emis",
            0
        )

        data["debt_to_income_ratio"] = customer.get(
            "debt_to_income_ratio",
            0
        )

        # =========================
        # CREDIT PROFILE
        # =========================
        data["cibil_score"] = customer.get(
            "cibil_score",
            650
        )

        data["credit_history"] = customer.get(
            "credit_history",
            0
        )

        data["default_history_count"] = customer.get(
            "default_history_count",
            0
        )

        data["number_of_previous_loans"] = customer.get(
            "number_of_previous_loans",
            0
        )

        # =========================
        # LOAN REQUEST
        # =========================
        data["loan_amount"] = loan_request.get(
            "loan_amount",
            0
        )

        data["loan_term_months"] = loan_request.get(
            "loan_term_months",
            0
        )

        data["purpose_of_loan"] = loan_request.get(
            "purpose_of_loan",
            "Unknown"
        )

        data["property_area"] = loan_request.get(
            "property_area",
            "Urban"
        )

        return pd.DataFrame([data])