CATEGORICAL_FEATURES = [
    "gender", "married", "education", "occupation",
    "employment_status", "business_type",
    "organization_type", "purpose_of_loan",
    "property_area"
]

NUMERICAL_FEATURES = [
    "age", "employment_length_years",
    "applicant_income", "coapplicant_income",
    "annual_household_income", "monthly_expense",
    "asset_value", "existing_emis",
    "debt_to_income_ratio", "cibil_score",
    "credit_history", "default_history_count",
    "number_of_previous_loans",
    "loan_amount", "loan_term_months",
    "total_income", "disposable_income",
    "emi_burden_ratio", "asset_to_income_ratio"
]

ALL_FEATURES = CATEGORICAL_FEATURES + NUMERICAL_FEATURES