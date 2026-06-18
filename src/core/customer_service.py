import pandas as pd
from sqlalchemy import text
from src.database.services.db_service import engine
import os
from dotenv import load_dotenv

load_dotenv()


class CustomerService:

    def __init__(self):
        self.engine = engine

    # =========================
    # CHECK CUSTOMER EXISTS
    # =========================
    def customer_exists(self, phone_number: str) -> bool:

        query = text("""
            SELECT 1
            FROM customers
            WHERE phone_number = :phone
        """)

        with self.engine.connect() as conn:
            result = conn.execute(query, {"phone": phone_number})
            row = result.fetchone()

        return row is not None

    # =========================
    # GET CUSTOMER PROFILE
    # =========================
    def get_customer_by_phone(self, phone_number: str):

        query = text("""
            SELECT
                c.customer_id,
                c.customer_name,
                c.age,
                c.gender,
                c.married,
                c.education,
                c.occupation,

                ep.employment_status,
                ep.employment_length_years,
                ep.business_type,
                ep.organization_type,

                fp.applicant_income,
                fp.coapplicant_income,
                fp.annual_household_income,
                fp.monthly_expense,
                fp.asset_value,
                fp.existing_emis,
                fp.debt_to_income_ratio,

                cp.cibil_score,
                cp.credit_history,
                cp.default_history_count,
                cp.number_of_previous_loans

            FROM customers c
            INNER JOIN employment_profiles ep
                ON c.customer_id = ep.customer_id
            INNER JOIN financial_profiles fp
                ON c.customer_id = fp.customer_id
            INNER JOIN credit_profiles cp
                ON c.customer_id = cp.customer_id

            WHERE c.phone_number = :phone
        """)

        with self.engine.connect() as conn:
            df = pd.read_sql(query, conn, params={"phone": phone_number})

        if df.empty:
            return None

        return df.iloc[0].to_dict()

    # =========================
    # SAFE WRAPPER (MAIN METHOD)
    # =========================
    def fetch_customer_context(self, phone_number: str):

        exists = self.customer_exists(phone_number)

        if not exists:
            return {
                "exists": False,
                "profile": None
            }

        profile = self.get_customer_by_phone(phone_number)

        return {
            "exists": True,
            "profile": profile
        }