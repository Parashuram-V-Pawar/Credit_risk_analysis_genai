from pydantic import BaseModel
from pydantic import field_validator


class CreditProfile(BaseModel):
    cibil_score: int
    credit_history: float
    default_history_count: int
    number_of_previous_loans: int
    employment_length_years: int

    @field_validator("cibil_score")
    @classmethod
    def validate_cibil(cls, value):
        if not 300 <= value <= 900:
            raise ValueError(
                "Invalid CIBIL score"
            )
        return value