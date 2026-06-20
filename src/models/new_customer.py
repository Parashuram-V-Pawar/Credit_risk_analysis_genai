from pydantic import BaseModel, Field, field_validator


class NewCustomerLoanRequest(BaseModel):

    customer_name: str = Field(..., min_length=2)
    phone_number: str
    age: int = Field(..., ge=18, le=100)
    gender: str
    married: str
    education: str
    occupation: str
    employment_status: str
    employment_length_years: float = Field(
        ...,
        ge=0
    )
    business_type: str = "N/A"
    organization_type: str
    applicant_income: float = Field(
        ...,
        gt=0
    )
    coapplicant_income: float = 0
    
    annual_household_income: float

    monthly_expense: float

    asset_value: float = 0
    existing_emis: float = 0
    loan_amount: float
    loan_term_months: int

    purpose_of_loan: str
    property_area: str

    @field_validator(
        "occupation",
        "employment_status",
        "organization_type",
        "purpose_of_loan",
        "property_area"
    )
    @classmethod
    def validate_required_text(cls, value):
        if not value.strip():
            raise ValueError(
                "Field cannot be empty"
            )
        return value

    @field_validator("business_type")
    @classmethod
    def validate_business_type(cls, value):
        if not value.strip():
            return "N/A"
        return value

    @field_validator("loan_amount")
    @classmethod
    def validate_loan_amount(cls, value):
        if value < 1000:
            raise ValueError(
                "Loan Amount cannot be less than ₹1,000"
            )
        return value
    
    @field_validator("gender")
    @classmethod
    def validate_gender(cls, value):
        if value == "Select Gender":
            raise ValueError("Please select Gender")
        return value
    
    @field_validator("married")
    @classmethod
    def validate_married(cls, value):
        if value == "Select":
            raise ValueError("Please select Marital status")
        return value

    @field_validator("education")
    @classmethod
    def validate_education(cls, value):
        if value == "Select":
            raise ValueError("Please select Education")
        return value
    
    @field_validator("annual_household_income")
    @classmethod
    def validate_household_income(cls, value):
        if value <= 0:
            raise ValueError(
                "Annual Household Income must be greater than 0"
            )
        return value

    @field_validator("monthly_expense")
    @classmethod
    def validate_monthly_expense(cls, value):
        if value <= 0:
            raise ValueError(
                "Monthly Expense must be greater than 0"
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
    
    @field_validator("phone_number")
    @classmethod
    def validate_phone(cls, value):
        if len(value) != 10:
            raise ValueError("Phone number must be exactly 10 digits")
        return value