from src.models.customer import Customer
from src.models.financial import FinancialProfile
from src.models.credit import CreditProfile
from src.models.loan import LoanApplication

def validate_row(row):
    customer = Customer(
        customer_id = row['Customer_ID'],
        customer_name=row["Customer_Name"],
        gender=row["Gender"],
        age=row["Age"],
        married=row["Married"],
        dependents=row["Dependents"],
        education=row["Education"],
        occupation=row["Occupation"],
        state=row["State"],
        city=row["City"],
        pin_code=str(row["PIN_Code"]),
        phone_number=str(row["Phone_Number"]),
        email=row["Email"]
    )

    financial = FinancialProfile(
        applicant_income=row["Applicant_Income"],
        coapplicant_income=row["Coapplicant_Income"],
        annual_household_income=row["Annual_Household_Income"],
        monthly_expense=row["Monthly_Expense"],
        existing_emis=row["Existing_EMIs"],
        asset_value=row["Asset_Value"]
    )

    credit = CreditProfile(
        cibil_score=row["CIBIL_Score"],
        credit_history=row["Credit_History"],
        default_history_count=row["Default_History_Count"],
        number_of_previous_loans=row["Number_of_Previous_Loans"],
        employment_length_years=row["Employment_Length_Years"]
    )

    loan = LoanApplication(
        loan_id=row["Loan_ID"],
        loan_amount=row["Loan_Amount"],
        loan_term_months=row["Loan_Term_Months"],
        purpose_of_loan=row["Purpose_of_Loan"],
        loan_status=row["Loan_Status"]
    )
    return True
