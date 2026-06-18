import streamlit as st

from src.core.investigation_engine import CreditInvestigationEngine
from src.core.customer_service import CustomerService

# =========================
# SAFE LAZY SINGLETON INIT
# =========================
@st.cache_resource
def get_engine():
    return CreditInvestigationEngine()

@st.cache_resource
def get_customer_service():
    return CustomerService()


# =========================
# UI HEADER
# =========================
st.title("🏦 Credit Risk Investigation System")


# =========================
# STEP 1: PHONE INPUT
# =========================
phone = st.text_input("Enter Customer Mobile Number")

customer_data = None
is_existing = False

customer_service = get_customer_service()
engine = get_engine()

if phone:
    try:
        exists = customer_service.customer_exists(phone)

        if exists:
            st.success("Existing Customer Found")

            customer_data = customer_service.get_customer_by_phone(phone)
            is_existing = True

            st.subheader("Customer Profile")
            st.json(customer_data)

        else:
            st.warning("New Customer - Please enter full details")

    except Exception as e:
        st.error(f"Customer lookup failed: {e}")


# =========================
# STEP 2A: EXISTING CUSTOMER
# =========================
if phone and is_existing:

    st.subheader("Loan Evaluation (Existing Customer)")
    st.json(customer_data)

    loan_amount = st.number_input("Loan Amount", 0.0, 1e7, 500000.0)
    loan_term_months = st.number_input("Loan Term (Months)", 6, 360, 60)
    purpose_of_loan = st.text_input("Purpose of Loan", "Home")
    property_area = st.text_input("Property Area", "Urban")

    if st.button("Evaluate Loan"):

        input_data = dict(customer_data)
        input_data.update({
            "loan_amount": loan_amount,
            "loan_term_months": loan_term_months,
            "purpose_of_loan": purpose_of_loan,
            "property_area": property_area
        })

        try:
            result = engine.evaluate_customer(input_data)

            st.subheader("📊 Result")
            st.json(result)

        except Exception as e:
            st.error(f"Evaluation failed: {e}")


# =========================
# STEP 2B: NEW CUSTOMER
# =========================
elif phone and not is_existing:

    with st.form("new_customer_form"):

        customer_name = st.text_input("Customer Name")
        age = st.number_input("Age", 18, 100, 30)
        gender = st.selectbox("Gender", ["Male", "Female"])
        married = st.selectbox("Married", ["Yes", "No"])
        education = st.selectbox("Education", ["Graduate", "Not Graduate"])
        occupation = st.text_input("Occupation", "Salaried")

        employment_status = st.text_input("Employment Status", "Employed")
        employment_length_years = st.number_input("Employment Length", 0.0, 40.0, 5.0)

        business_type = st.text_input("Business Type", "N/A")
        organization_type = st.text_input("Organization Type", "Private")

        applicant_income = st.number_input("Applicant Income", 0.0, 1e7, 50000.0)
        coapplicant_income = st.number_input("Co-applicant Income", 0.0, 1e7, 0.0)
        annual_household_income = st.number_input("Household Income", 0.0, 1e7, 600000.0)
        monthly_expense = st.number_input("Monthly Expense", 0.0, 1e6, 20000.0)

        asset_value = st.number_input("Asset Value", 0.0, 1e8, 1000000.0)
        existing_emis = st.number_input("Existing EMIs", 0.0, 1e6, 5000.0)

        loan_amount = st.number_input("Loan Amount", 0.0, 1e7, 500000.0)
        loan_term_months = st.number_input("Loan Term", 6, 360, 60)
        purpose_of_loan = st.text_input("Purpose", "Home")
        property_area = st.text_input("Property Area", "Urban")

        submit = st.form_submit_button("Evaluate")

        if submit:

            input_data = {
                "customer_name": customer_name,
                "age": age,
                "gender": gender,
                "married": married,
                "education": education,
                "occupation": occupation,

                "employment_status": employment_status,
                "employment_length_years": employment_length_years,
                "business_type": business_type,
                "organization_type": organization_type,

                "applicant_income": applicant_income,
                "coapplicant_income": coapplicant_income,
                "annual_household_income": annual_household_income,
                "monthly_expense": monthly_expense,
                "asset_value": asset_value,
                "existing_emis": existing_emis,

                # NTC defaults
                "is_new_customer": True,
                "cibil_score": 650,
                "credit_history": 0,
                "default_history_count": 0,
                "number_of_previous_loans": 0,

                "loan_amount": loan_amount,
                "loan_term_months": loan_term_months,
                "purpose_of_loan": purpose_of_loan,
                "property_area": property_area
            }

            try:
                result = engine.evaluate_customer(input_data)

                st.subheader("📊 Result")
                st.json(result)

            except Exception as e:
                st.error(f"Evaluation failed: {e}")