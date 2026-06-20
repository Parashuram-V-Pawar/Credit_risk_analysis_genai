from fastapi import APIRouter
from fastapi import HTTPException

from src.core.investigation_engine import CreditInvestigationEngine
from src.models.new_customer import NewCustomerLoanRequest
from src.models.existing_customer import ExistingCustomerLoanRequest
from src.core.customer_service import CustomerService

router = APIRouter(
    prefix="/investigation",
    tags=["Investigation"]
)

engine = CreditInvestigationEngine()
customer_service = CustomerService()

@router.post("/existing")
def investigate_existing(request: ExistingCustomerLoanRequest):
    try:
        customer = customer_service.get_customer_by_id(
            request.customer_id
        )

        if not customer:
            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )

        input_data = dict(customer)
        input_data.update(request.model_dump())

        result = engine.evaluate_customer(input_data)

        loan_id = customer_service.create_loan_application(
            customer_id=request.customer_id,
            input_data=input_data,
            result=result
        )

        result["loan_id"] = loan_id
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
import logging
logger = logging.getLogger(__name__)

@router.post("/new")
def investigate_new(request: NewCustomerLoanRequest):
    try:
        input_data = request.model_dump()

        input_data.update({
            "is_new_customer": True,
            "cibil_score": 650,
            "credit_history": 0,
            "default_history_count": 0,
            "number_of_previous_loans": 0
        })

        result = engine.evaluate_customer(input_data)

        customer_id = customer_service.create_new_customer(input_data)

        loan_id = customer_service.create_loan_application(
            customer_id=customer_id,
            input_data=input_data,
            result=result
        )

        return {
            **result,
            "customer_id": customer_id,
            "loan_id": loan_id
        }

    except Exception as e:
        logger.exception("Error in /investigation/new")
        raise HTTPException(status_code=500, detail=str(e))