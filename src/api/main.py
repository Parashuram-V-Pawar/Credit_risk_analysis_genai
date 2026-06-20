from fastapi import FastAPI

from src.api.routes.customer import router as customer_router
from src.api.routes.investigation import router as investigation_router

app = FastAPI(
    title="Credit Risk Investigation API",
    version="1.0.0",
    description="Loan Approval & Risk Investigation Platform"
)

app.include_router(customer_router)
app.include_router(investigation_router)


@app.get("/")
def home():
    return {
        "message": "Credit Risk Investigation API Running"
    }