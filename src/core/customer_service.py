import pandas as pd
import sqlite3

from sqlalchemy import text
from datetime import datetime
from uuid import uuid4

from src.database.services.db_service import engine
import os
from dotenv import load_dotenv

load_dotenv()


class CustomerService:

    def __init__(self):
        self.engine = engine

    # =========================
    # GENERATES CUSTOMER ID's
    # =========================
    def generate_customer_id(self):
        return f"CUST{uuid4().hex[:8].upper()}"
    
    # =========================
    # GENERATES LOAN ID's
    # =========================
    def generate_loan_id(self):
        return f"LOAN{uuid4().hex[:8].upper()}"

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
    
    def get_customer_by_id(self, customer_id: str):
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

            WHERE c.customer_id = :customer_id
        """)

        with self.engine.connect() as conn:
            df = pd.read_sql(
                query,
                conn,
                params={
                    "customer_id": customer_id
                }
            )

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
    
    def create_new_customer(self, customer_data: dict):
        customer_id = self.generate_customer_id()
        debt_ratio = 0

        if customer_data["applicant_income"] > 0:
            debt_ratio = (
                customer_data["existing_emis"]
                / customer_data["applicant_income"]
            )

        with self.engine.begin() as conn:
            # =========================
            # CUSTOMERS
            # =========================
            conn.execute(
                text("""
                    INSERT INTO customers (
                        customer_id,
                        customer_name,
                        phone_number,
                        gender,
                        age,
                        married,
                        education,
                        occupation,
                        created_at
                    )
                    VALUES (
                        :customer_id,
                        :customer_name,
                        :phone_number,
                        :gender,
                        :age,
                        :married,
                        :education,
                        :occupation,
                        :created_at
                    )
                """),
                {
                    "customer_id": customer_id,
                    "customer_name": customer_data["customer_name"],
                    "phone_number": customer_data["phone_number"],
                    "gender": customer_data["gender"],
                    "age": customer_data["age"],
                    "married": customer_data["married"],
                    "education": customer_data["education"],
                    "occupation": customer_data["occupation"],
                    "created_at": datetime.now()
                }
            )

            # =========================
            # EMPLOYMENT PROFILE
            # =========================
            conn.execute(
                text("""
                    INSERT INTO employment_profiles (
                        customer_id,
                        employment_status,
                        employment_length_years,
                        business_type,
                        organization_type
                    )
                    VALUES (
                        :customer_id,
                        :employment_status,
                        :employment_length_years,
                        :business_type,
                        :organization_type
                    )
                """),
                {
                    "customer_id": customer_id,
                    "employment_status":
                        customer_data["employment_status"],
                    "employment_length_years":
                        customer_data["employment_length_years"],
                    "business_type":
                        customer_data.get("business_type", "N/A"),
                    "organization_type":
                        customer_data["organization_type"]
                }
            )

            # =========================
            # FINANCIAL PROFILE
            # =========================
            conn.execute(
                text("""
                    INSERT INTO financial_profiles (
                        customer_id,
                        applicant_income,
                        coapplicant_income,
                        annual_household_income,
                        monthly_expense,
                        asset_value,
                        existing_emis,
                        debt_to_income_ratio
                    )
                    VALUES (
                        :customer_id,
                        :applicant_income,
                        :coapplicant_income,
                        :annual_household_income,
                        :monthly_expense,
                        :asset_value,
                        :existing_emis,
                        :debt_to_income_ratio
                    )
                """),
                {
                    "customer_id": customer_id,
                    "applicant_income":
                        customer_data["applicant_income"],
                    "coapplicant_income":
                        customer_data["coapplicant_income"],
                    "annual_household_income":
                        customer_data["annual_household_income"],
                    "monthly_expense":
                        customer_data["monthly_expense"],
                    "asset_value":
                        customer_data["asset_value"],
                    "existing_emis":
                        customer_data["existing_emis"],
                    "debt_to_income_ratio":
                        debt_ratio
                }
            )

            # =========================
            # CREDIT PROFILE
            # =========================
            conn.execute(
                text("""
                    INSERT INTO credit_profiles (
                        customer_id,
                        cibil_score,
                        credit_history,
                        default_history_count,
                        number_of_previous_loans
                    )
                    VALUES (
                        :customer_id,
                        :cibil_score,
                        :credit_history,
                        :default_history_count,
                        :number_of_previous_loans
                    )
                """),
                {
                    "customer_id": customer_id,
                    "cibil_score":
                        customer_data["cibil_score"],
                    "credit_history":
                        customer_data["credit_history"],
                    "default_history_count":
                        customer_data["default_history_count"],
                    "number_of_previous_loans":
                        customer_data["number_of_previous_loans"]
                }
            )
        return customer_id
    
    def create_loan_application(self, customer_id: str, input_data: dict, result: dict):
        loan_id = self.generate_loan_id()

        with self.engine.begin() as conn:
            conn.execute(
                text("""
                    INSERT INTO loan_applications (
                        loan_id,
                        customer_id,
                        loan_amount,
                        loan_term_months,
                        purpose_of_loan,
                        property_area,
                        loan_status,
                        application_date
                    )
                    VALUES (
                        :loan_id,
                        :customer_id,
                        :loan_amount,
                        :loan_term_months,
                        :purpose_of_loan,
                        :property_area,
                        :loan_status,
                        :application_date
                    )
                """),
                {
                    "loan_id": loan_id,
                    "customer_id": customer_id,
                    "loan_amount":
                        input_data["loan_amount"],
                    "loan_term_months":
                        input_data["loan_term_months"],
                    "purpose_of_loan":
                        input_data["purpose_of_loan"],
                    "property_area":
                        input_data["property_area"],
                    "loan_status":
                        result["final_decision"],
                    "application_date":
                        datetime.now()
                }
            )
        return loan_id