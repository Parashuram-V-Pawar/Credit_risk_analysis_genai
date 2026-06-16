import pandas as pd

from pydantic import ValidationError

from src.data_preprocess.data_validation import validate_row
from src.data_preprocess.data_cleaning import clean_customers_data


RAW_DATASET = "dataset/raw/hdfc_loan_dataset_full_enriched.csv"
PROCESSED_DATASET = "dataset/processed/cleaned_dataset.csv"
REJECTED_DATASET = "dataset/processed/rejected_records.csv"

def standardize_columns(df: pd.DataFrame):
    column_mapping = {
        "Loan_ID": "loan_id",
        "Bank": "bank_name",
        "Customer_Name": "customer_name",
        "Gender": "gender",
        "Married": "married",
        "Dependents": "dependents",
        "Education": "education",
        "Employment_Status": "employment_status",
        "Applicant_Income": "applicant_income",
        "Coapplicant_Income": "coapplicant_income",
        "Loan_Amount": "loan_amount",
        "Loan_Term_Months": "loan_term_months",
        "Credit_History": "credit_history",
        "Property_Area": "property_area",
        "Age": "age",
        "Loan_Status": "loan_status",
        "CIBIL_Score": "cibil_score",
        "Annual_Household_Income": "annual_household_income",
        "Debt_to_Income_Ratio": "debt_to_income_ratio",
        "Purpose_of_Loan": "purpose_of_loan",
        "Existing_EMIs": "existing_emis",
        "Number_of_Previous_Loans": "number_of_previous_loans",
        "Default_History_Count": "default_history_count",
        "Employment_Length_Years": "employment_length_years",
        "Business_Type": "business_type",
        "Asset_Value": "asset_value",
        "Guarantor": "guarantor",
        "Co-signer_Relationship": "cosigner_relationship",
        "Monthly_Expense": "monthly_expense",
        "Organization_Type": "organization_type",
        "Region_Branch": "region_branch",
        "Mobile_Verified": "mobile_verified",
        "Email_Verified": "email_verified",
        "Institutional_Relationships": "institutional_relationships",
        "Application_Text": "application_text",
        "Customer_Feedback": "customer_feedback",
        "Agent_Notes": "agent_notes",
        "Loan_to_Annual_Income": "loan_to_annual_income",
        "Customer_Sentiment": "customer_sentiment",
        "Religion": "religion",
        "State": "state",
        "City": "city",
        "PIN_Code": "pin_code",
        "Aadhaar_Synthetic": "aadhaar_synthetic",
        "Phone_Number": "phone_number",
        "Email": "email",
        "Occupation": "occupation",
        "Customer_ID": "customer_id"
    }
    return df.rename(columns=column_mapping)


def main():
    print("=" * 50)
    print("LOADING DATASET")
    print("=" * 50)

    df = pd.read_csv(RAW_DATASET)

    df = clean_customers_data(df)
    df["Customer_ID"] = [f"CUST{i:06d}" for i in range(1, len(df)+1)]
    
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

    cleaned_df = standardize_columns(df)
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