from pydantic import BaseModel
from pydantic import field_validator


class FinancialProfile(BaseModel):
    applicant_income: float
    coapplicant_income: float
    annual_household_income: float
    monthly_expense: float
    existing_emis: float
    asset_value: float

    @field_validator(
        "applicant_income",
        "annual_household_income",
        "asset_value"
    )
    @classmethod
    def validate_positive(cls, value):
        if value < 0:
            raise ValueError(
                "Value must be positive"
            )
        return value