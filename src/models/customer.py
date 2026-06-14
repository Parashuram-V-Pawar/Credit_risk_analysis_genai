from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import field_validator


class Customer(BaseModel):
    customer_name: str
    gender: str
    age: int
    married: str
    dependents: int
    education: str
    occupation: str
    state: str
    city: str
    pin_code: str
    phone_number: str
    email: EmailStr

    @field_validator("age")
    @classmethod
    def validate_age(cls, value):
        if not 18 <= value <= 80:
            raise ValueError(
                "Age must be between 18 and 80"
            )
        return value