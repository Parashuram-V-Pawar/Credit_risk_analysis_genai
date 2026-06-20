from pydantic import BaseModel, field_validator


class PhoneRequest(BaseModel):
    phone: str

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):

        value = value.strip()

        if not value.isdigit():
            raise ValueError(
                "Mobile number must contain only digits"
            )

        if len(value) != 10:
            raise ValueError(
                "Mobile number must be exactly 10 digits"
            )

        return value