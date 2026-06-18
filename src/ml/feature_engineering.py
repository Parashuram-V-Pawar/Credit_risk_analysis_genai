import pandas as pd

def create_features(df):
    
    def safe(col):
        return df[col] if col in df.columns else 0

    df["total_income"] = (
        safe("applicant_income") +
        safe("coapplicant_income")
    )

    df["disposable_income"] = (
        df["total_income"]
        - safe("monthly_expense")
        - safe("existing_emis")
    )

    df["emi_burden_ratio"] = (
        safe("existing_emis") / (df["total_income"] + 1)
    )

    df["debt_to_income_ratio"] = (
        safe("existing_emis") / (df["total_income"] + 1)
    )

    df["asset_to_income_ratio"] = (
        safe("asset_value") / (safe("annual_household_income") + 1)
    )

    df["loan_to_annual_income"] = (
        safe("loan_amount") / (safe("annual_household_income") + 1)
    )

    return df