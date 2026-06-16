from src.database.services.db_service import engine

def customer_insert(df):
    customers_df = df[
            [
                "customer_id", "customer_name",
                "aadhaar_synthetic", "phone_number",
                "email", "gender", "age", "religion",
                "married", "dependents", "education",
                "occupation", "state", "city", "pin_code"
            ]
        ].copy()

    customers_df.to_sql(
        "customers",
        engine,
        if_exists="append",
        index=False
    )
    print("Successful")

def employment_profiles_insert(df):
    employment_df = df[
        [
            "customer_id",
            "employment_status",
            "employment_length_years",
            "business_type",
            "organization_type"
        ]
    ].copy()

    employment_df.to_sql(
        "employment_profiles",
        engine,
        if_exists="append",
        index=False
    )

def financial_profiles_insert(df):
    financial_df = df[
        [
            "customer_id", "applicant_income",
            "coapplicant_income", "annual_household_income",
            "monthly_expense", "asset_value",
            "existing_emis", "debt_to_income_ratio"
        ]
    ].copy()

    financial_df.to_sql(
        "financial_profiles",
        engine,
        if_exists="append",
        index=False
    )

def credit_profiles_insert(df):
    credit_df = df[
        [
            "customer_id", "cibil_score",
            "credit_history", "default_history_count",
            "number_of_previous_loans"
        ]
    ].copy()

    credit_df.to_sql(
        "credit_profiles",
        engine,
        if_exists="append",
        index=False
    )

def loan_applications_insert(df):
    loan_df = df[
        [
            "loan_id", "customer_id",
            "bank_name", "loan_amount",
            "loan_term_months", "purpose_of_loan",
            "property_area", "guarantor",
            "cosigner_relationship", "loan_status"
        ]
    ].copy()

    loan_df.to_sql(
        "loan_applications",
        engine,
        if_exists="append",
        index=False
    )