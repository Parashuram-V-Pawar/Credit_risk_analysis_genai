from fastapi import APIRouter, HTTPException

from src.core.customer_service import CustomerService

router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)

customer_service = CustomerService()


@router.get("/{phone}")
def get_customer(phone: str):

    customer = customer_service.get_customer_by_phone(
        phone
    )

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return customer