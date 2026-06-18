import pandas as pd

class FeatureBuilder:

    def build(self, customer, loan_request):

        data = {}

        # --------------------
        # CUSTOMER FIELDS
        # --------------------
        data["age"] = customer.get("age")
        data["gender"] = customer.get("gender")
        data["married"] = customer.get("married")
        data["education"] = customer.get("education")
        data["occupation"] = customer.get("occupation")

        # employment
        data["employment_status"] = customer.get("employment_status")
        data["employment_length_years"] = customer.get("employment_length_years")
        data["business_type"] = customer.get("business_type")
        data["organization_type"] = customer.get("organization_type")

        # financial
        data["applicant_income"] = customer.get("applicant_income")
        data["coapplicant_income"] = customer.get("coapplicant_income")
        data["annual_household_income"] = customer.get("annual_household_income")
        data["monthly_expense"] = customer.get("monthly_expense")
        data["asset_value"] = customer.get("asset_value")
        data["existing_emis"] = customer.get("existing_emis")
        data["debt_to_income_ratio"] = customer.get("debt_to_income_ratio")

        # credit
        data["cibil_score"] = customer.get("cibil_score")
        data["credit_history"] = customer.get("credit_history")
        data["default_history_count"] = customer.get("default_history_count")
        data["number_of_previous_loans"] = customer.get("number_of_previous_loans")

        # loan request
        data["loan_amount"] = loan_request["loan_amount"]
        data["loan_term_months"] = loan_request["loan_term_months"]
        data["purpose_of_loan"] = loan_request.get("purpose_of_loan")
        data["property_area"] = loan_request.get("property_area")

        return pd.DataFrame([data])