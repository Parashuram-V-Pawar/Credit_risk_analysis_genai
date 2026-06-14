import pandas as pd

from pydantic import ValidationError

from src.models.customer import Customer
from src.models.financial import FinancialProfile
from src.models.credit import CreditProfile
from src.models.loan import LoanApplication


RAW_DATASET = "dataset/raw/hdfc_loan_dataset_full_enriched.csv"
PROCESSED_DATASET = "dataset/processed/cleaned_dataset.csv"
REJECTED_DATASET = "dataset/processed/rejected_records.csv"


def validate_row(row):
    customer = Customer(
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


def main():
    print("=" * 50)
    print("LOADING DATASET")
    print("=" * 50)

    df = pd.read_csv(RAW_DATASET)
    print(f"Total Rows : {len(df)}")
    print(f"Total Columns : {len(df.columns)}")

    valid_records = []
    invalid_records = []

    for index, row in df.iterrows():
        try:
            validate_row(row)
            valid_records.append(
                row.to_dict()
            )
        except ValidationError as e:
            invalid_records.append(
                {
                    "row_number": index,
                    "loan_id": row.get(
                        "Loan_ID",
                        None
                    ),
                    "error": str(e)
                }
            )

    cleaned_df = pd.DataFrame(valid_records)
    rejected_df = pd.DataFrame(invalid_records)

    cleaned_df.to_csv(PROCESSED_DATASET, index=False)
    rejected_df.to_csv(REJECTED_DATASET, index=False)

    print("\n")
    print("=" * 50)
    print("VALIDATION REPORT")
    print("=" * 50)
    print(f"Valid Records : {len(cleaned_df)}")
    print(f"Rejected Records : {len(rejected_df)}")
    print("\n")
    print(f"Saved : {PROCESSED_DATASET}")
    print(f"Saved : {REJECTED_DATASET}")


if __name__ == "__main__":
    main()