import pandas as pd

def create_features(df):

    # total household income
    df["total_income"] = (
        df["applicant_income"] +
        df["coapplicant_income"]
    )

    # annual disposable income
    df["disposable_income"] = (
        df["annual_household_income"] -
        (df["monthly_expense"] * 12)
    )

    # EMI burden
    df["emi_burden_ratio"] = (
        df["existing_emis"] /
        (df["total_income"] + 1)
    )

    # Debt to Income ratio
    df["debt_to_income_ratio"] = (
        df["monthly_expense"] + df["existing_emis"]
    ) / (
        (df["annual_household_income"] / 12) + 1
    )
    
    # assets relative to income
    df["asset_to_income_ratio"] = (
        df["asset_value"] /
        (df["annual_household_income"] + 1)
    )

    # loan relative to income
    df["loan_to_annual_income"] = (
        df["loan_amount"] /
        (df["annual_household_income"] + 1)
    )

    return df


def get_approval_model_features():
    return [
        "age",
        "gender",
        "married",
        "education",
        "occupation",
        "employment_status",
        "employment_length_years",
        "business_type",
        "organization_type",

        "applicant_income",
        "coapplicant_income",
        "annual_household_income",
        "monthly_expense",
        "asset_value",
        "existing_emis",

        "debt_to_income_ratio",
        "cibil_score",
        "credit_history",
        "default_history_count",
        "number_of_previous_loans",

        "loan_amount",
        "loan_term_months",
        "purpose_of_loan",
        "property_area",

        # engineered features
        "total_income",
        "disposable_income",
        "emi_burden_ratio",
        "asset_to_income_ratio",
        "loan_to_annual_income"
    ]

def get_credit_score_features():
    return [
        "age",
        "employment_length_years",

        "total_income",
        "disposable_income",
        "emi_burden_ratio",
        "asset_to_income_ratio",
        "loan_to_annual_income",

        "gender",
        "married",
        "education",
        "occupation",
        "employment_status",
        "business_type",
        "organization_type",
    ]