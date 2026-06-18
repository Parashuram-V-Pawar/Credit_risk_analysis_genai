from pydantic import BaseModel
from typing import Optional


# =========================
# BASE FIELDS (COMMON)
# =========================
class LoanRequest(BaseModel):
    phone_number: str
    loan_amount: float
    loan_term_months: int
    purpose_of_loan: Optional[str] = None


# =========================
# NEW CUSTOMER INPUT
# =========================
class NewCustomerRequest(LoanRequest):
    customer_name: str
    age: int
    gender: str
    married: Optional[str] = None
    dependents: Optional[int] = 0
    education: Optional[str] = None

    occupation: Optional[str] = None
    employment_status: str
    employment_length_years: Optional[int] = 0

    applicant_income: float
    coapplicant_income: Optional[float] = 0
    annual_household_income: float
    monthly_expense: float
    existing_emis: Optional[float] = 0

    property_area: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pin_code: Optional[str] = None