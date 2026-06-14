from pydantic import BaseModel
from pydantic import field_validator


class LoanApplication(BaseModel):
    loan_id: str
    loan_amount: float
    loan_term_months: int
    purpose_of_loan: str
    loan_status: str

    @field_validator("loan_amount")
    @classmethod
    def validate_amount(cls, value):
        if value <= 0:
            raise ValueError(
                "Loan amount must be positive"
            )
        return value