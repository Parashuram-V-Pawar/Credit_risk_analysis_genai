import pandas as pd

from src.database.services.db_service import engine


def load_credit_training_data() -> pd.DataFrame:
    query = """
    SELECT
        c.customer_id, c.age, c.gender, c.married,
        c.education, c.occupation,

        ep.employment_length_years,
        ep.employment_status, ep.business_type,
        ep.organization_type,

        fp.applicant_income, fp.coapplicant_income,
        fp.annual_household_income,
        fp.monthly_expense, fp.existing_emis,
        fp.asset_value, fp.debt_to_income_ratio,

        cp.cibil_score, cp.credit_history,
        cp.default_history_count,
        cp.number_of_previous_loans,

        la.loan_amount,
        (
            la.loan_amount /
            NULLIF(fp.annual_household_income,0)
        ) AS loan_to_annual_income
    FROM customers c

    JOIN employment_profiles ep
    ON c.customer_id = ep.customer_id

    JOIN financial_profiles fp
    ON c.customer_id = fp.customer_id

    JOIN credit_profiles cp
    ON c.customer_id = cp.customer_id

    JOIN loan_applications la
    ON c.customer_id = la.customer_id
    """
    return pd.read_sql(query, engine)


def load_loan_approval_training_data() -> pd.DataFrame:
    query = """
    SELECT
        c.age, c.gender, c.married, 
        c.education,c.occupation,

        ep.employment_status, ep.employment_length_years,
        ep.business_type, ep.organization_type,

        fp.applicant_income, fp.coapplicant_income,
        fp.annual_household_income, fp.monthly_expense,
        fp.asset_value, fp.existing_emis,
        fp.debt_to_income_ratio,

        cp.cibil_score, cp.credit_history,
        cp.default_history_count,
        cp.number_of_previous_loans,

        la.loan_amount, la.loan_term_months,
        la.purpose_of_loan, la.property_area,
        la.loan_status
    FROM customers c

    INNER JOIN employment_profiles ep
        ON c.customer_id = ep.customer_id

    INNER JOIN financial_profiles fp
        ON c.customer_id = fp.customer_id

    INNER JOIN credit_profiles cp
        ON c.customer_id = cp.customer_id

    INNER JOIN loan_applications la
        ON c.customer_id = la.customer_id
    """

    return pd.read_sql(query, engine)