from sqlalchemy import text
from src.database.services.db_service import engine


class DBClient:

    def __init__(self):
        self.engine = engine
        
    # =========================
    # 1. CUSTOMER LOOKUP
    # =========================
    def get_customer_by_phone(self, phone_number: str):

        query = """
        SELECT TOP 1
            c.customer_id,
            c.customer_name,
            c.phone_number,
            c.email,
            c.age,
            c.gender,
            c.occupation,
            ep..employment_status
        FROM customers

        Left JOIN employement_profiles ep
            ON ep.customer_id = c.customer_id
        WHERE phone_number = :phone
        """

        with engine.connect() as conn:
            result = conn.execute(text(query), {"phone": phone_number}).fetchone()

        return dict(result._mapping) if result else None


    # =========================
    # 2. CREDIT PROFILE FETCH
    # =========================
    def get_credit_profile(self, customer_id: str):

        query = """
        SELECT
            customer_id,
            cibil_score,
            credit_history,
            default_history_count,
            number_of_previous_loans,
            asset_value
        FROM credit_profiles
        WHERE customer_id = :cid
        """

        with engine.connect() as conn:
            result = conn.execute(text(query), {"cid": customer_id}).fetchone()

        return dict(result._mapping) if result else {}


    # =========================
    # 3. CREATE NEW CUSTOMER
    # =========================
    def create_customer(self, data: dict):

        query = """
        INSERT INTO customers (
            customer_name,
            phone_number,
            email,
            age,
            gender,
            occupation,
            employment_status,
            created_at
        )
        VALUES (
            :customer_name,
            :phone_number,
            :email,
            :age,
            :gender,
            :occupation,
            :employment_status,
            GETDATE()
        )
        """

        with engine.begin() as conn:
            conn.execute(text(query), data)


    # =========================
    # 4. STORE INVESTIGATION RESULT
    # =========================
    def store_investigation(self, data: dict):

        query = """
        INSERT INTO loan_applications (
            customer_id,
            phone_number,
            loan_amount,
            loan_term_months,
            decision,
            probability,
            risk_score,
            risk_band,
            explanation,
            created_at
        )
        VALUES (
            :customer_id,
            :phone_number,
            :loan_amount,
            :loan_term_months,
            :decision,
            :probability,
            :risk_score,
            :risk_band,
            :explanation,
            GETDATE()
        )
        """

        with engine.begin() as conn:
            conn.execute(text(query), data)

    def get_full_customer_profile(self, phone_number: str):

            query = text("""
            SELECT TOP 1
                c.customer_id,
                c.customer_name,
                c.phone_number,
                c.email,
                c.gender,
                c.age,
                c.married,
                c.education,
                c.occupation,
                c.state,
                c.city,
                c.pin_code,

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
            LEFT JOIN employment_profiles ep
                ON c.customer_id = ep.customer_id
            LEFT JOIN financial_profiles fp
                ON c.customer_id = fp.customer_id
            LEFT JOIN credit_profiles cp
                ON c.customer_id = cp.customer_id

            WHERE c.phone_number = :phone
            """)

            with self.engine.connect() as conn:
                result = conn.execute(query, {"phone": phone_number}).fetchone()

            if not result:
                return None

            return dict(result._mapping)