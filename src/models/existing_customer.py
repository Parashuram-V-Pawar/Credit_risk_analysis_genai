from pydantic import BaseModel, field_validator


class ExistingCustomerLoanRequest(BaseModel):

    customer_id: str
    loan_amount: float
    loan_term_months: int
    purpose_of_loan: str
    property_area: str

    @field_validator("loan_amount")
    @classmethod
    def validate_loan_amount(cls, value):
        if value < 1000:
            raise ValueError(
                "Loan Amount cannot be less than ₹1000"
            )
        return value

    @field_validator("loan_term_months")
    @classmethod
    def validate_loan_term(cls, value):
        if value < 6:
            raise ValueError(
                "Loan Term must be at least 6 months"
            )
        return value