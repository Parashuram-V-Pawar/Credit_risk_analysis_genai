import streamlit as st
import pandas as pd

from pydantic import ValidationError

from src.core.investigation_engine import CreditInvestigationEngine
from src.core.customer_service import CustomerService
from src.models.phone_validator import PhoneRequest
from src.models.new_customer import NewCustomerLoanRequest
from src.models.existing_customer import ExistingCustomerLoanRequest


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
st.set_page_config(
    page_title="Credit Risk Investigation",
    page_icon="🏦",
    layout="wide"
)

st.title("🏦 Credit Risk Investigation Platform")
st.caption("AI-Powered Loan Approval, Risk Assessment & Investigation")

# =========================
# NEW CUSTOMER RESULT DASHBOARD
# =========================
def show_result_dashboard(result):
    st.success("Investigation Completed")
    st.divider()
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(
        "Approval %",
        f"{result['approval_probability'] * 100:.1f}%"
    )
    col2.metric(
        "Default %",
        f"{result['default_probability'] * 100:.1f}%"
    )
    col3.metric(
        "Risk Score",
        f"{result['risk_score']:.0f}"
    )
    col4.metric(
        "Risk Level",
        result["risk_level"]
    )
    st.divider()
    decision = result["final_decision"]

    if decision == "APPROVED":
        st.success("✅ LOAN APPROVED")

    elif decision == "CONDITIONAL_APPROVAL":
        st.warning("⚠️ CONDITIONAL APPROVAL")
        if result.get("conditions"):
            st.subheader("Required Conditions")
            for condition in result["conditions"]:
                st.write(f"• {condition}")

    else:
        st.error("❌ LOAN REJECTED")
    st.divider()

    st.subheader("📄 Credit Investigation Report")

    st.markdown(
        result["final_report"]
    )

    # if result.get("similar_cases"):
    #     st.divider()
    #     st.subheader("📚 Similar Historical Cases")

    #     for idx, case in enumerate(
    #         result["similar_cases"],
    #         start=1
    #     ):
    #         with st.expander(f"Case {idx}"):
    #             st.text(case)

    if result.get("policy_context"):
        st.divider()
        st.subheader("📖 Relevant Policy Guidance")

        if isinstance(result["policy_context"], list):
            for idx, policy in enumerate(
                result["policy_context"],
                start=1
            ):
                with st.expander(f"Policy {idx}"):
                    st.text(policy)
        else:
            st.text(result["policy_context"])

# =========================
# STEP 1: PHONE INPUT
# =========================
phone = st.text_input(
    "Enter Customer Mobile Number",
    placeholder="Enter 10-digit mobile number"
)
customer_data = None
is_existing = False

customer_service = get_customer_service()
engine = get_engine()

if phone:
    try:
        validated_phone = PhoneRequest(phone=phone)
        phone = validated_phone.phone

    except ValidationError as e:
        for error in e.errors():
            st.error(error["msg"])
        st.stop()

if phone:
    try:
        exists = customer_service.customer_exists(phone)
        if exists:
            st.success("Existing Customer Found")

            customer_data = customer_service.get_customer_by_phone(phone)
            is_existing = True

            st.subheader(f"👤 {customer_data['customer_name']}")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Customer ID", customer_data.get("customer_id", "-"))
                st.metric("Age", customer_data.get("age", "-"))

            with col2:
                st.metric("CIBIL Score", customer_data.get("cibil_score", "-"))
                st.metric(
                    "Previous Loans",
                    customer_data.get("number_of_previous_loans", "-")
                )

            with col3:
                st.metric(
                    "Annual Income",
                    f"₹{customer_data.get('annual_household_income', 0):,.0f}"
                )
                st.metric(
                    "Defaults",
                    customer_data.get("default_history_count", "-")
                )

            with st.expander("View Full Customer Details"):

                customer_df = pd.DataFrame(
                    customer_data.items(),
                    columns=["Field", "Value"]
                )

                st.dataframe(
                    customer_df,
                    use_container_width=True,
                    hide_index=True
                )
        else:
            st.warning("New Customer - Please enter full details")

    except Exception as e:
        st.error(f"Customer lookup failed: {e}")


# =========================
# STEP 2A: EXISTING CUSTOMER
# =========================
if phone and is_existing:
    st.subheader("Loan Evaluation (Existing Customer)")
    st.subheader("🏦 Loan Request Details")

    col1, col2 = st.columns(2)

    with col1:
        st.write(
            f"**Customer:** {customer_data['customer_name']}"
        )
        st.write(
            f"**CIBIL Score:** {customer_data['cibil_score']}"
        )

    with col2:
        st.write(
            f"**Annual Income:** ₹{customer_data['annual_household_income']:,.0f}"
        )
        st.write(
            f"**Previous Loans:** {customer_data['number_of_previous_loans']}"
        )

    loan_amount = st.number_input("Loan Amount", 1000.0, 1e7, 500000.0)
    loan_term_months = st.number_input("Loan Term (Months)", 6, 360, 60)
    purpose_of_loan = st.text_input("Purpose of Loan", "Home")
    property_area = st.text_input("Property Area", "Urban")

    if st.button("Evaluate Loan", key="existing_customer_eval"):

        try:
            validated_request = ExistingCustomerLoanRequest(
                customer_id=customer_data["customer_id"],
                loan_amount=loan_amount,
                loan_term_months=loan_term_months,
                purpose_of_loan=purpose_of_loan,
                property_area=property_area
            )

        except ValidationError as e:
            for error in e.errors():
                st.error(
                    f"{error['loc'][0]}: {error['msg']}"
                )
            st.stop()

        input_data = dict(customer_data)
        
        input_data.update(
            validated_request.model_dump()
        )
        
        try:
            with st.spinner("Running credit investigation..."):
                result = engine.evaluate_customer(input_data)
                loan_id = customer_service.create_loan_application(customer_data["customer_id"], 
                                                                   input_data, result)
            show_result_dashboard(result)

        except Exception as e:
            st.error(f"Evaluation failed: {e}")


# =========================
# STEP 2B: NEW CUSTOMER
# =========================
elif phone and not is_existing:
    with st.form("new_customer_form"):

        customer_name = st.text_input(
            "Customer Name *",
            placeholder="Enter full name"
        )

        phone_number = st.text_input(
            "Phone Number *",
            value=phone,
            placeholder="10-digit mobile number"
        )
        
        age = st.number_input("Age", 18, 100, 30)

        gender = st.selectbox(
            "Gender *",
            ["Select Gender", "Male", "Female"]
        )
        

        married = st.selectbox(
            "Marital Status *",
            ["Select", "Yes", "No"]
        )

        education = st.selectbox(
            "Education *",
            ["Select", "Graduate", "Not Graduate"]
        )

        occupation = st.text_input(
            "Occupation *",
            placeholder="e.g. Software Engineer"
        )

        employment_status = st.text_input(
            "Employment Status *",
            placeholder="e.g. Employed, Self-Employed"
        )
        employment_length_years = st.number_input("Employment Length", 0.0, 40.0, 5.0)

        business_type = st.text_input(
            "Business Type",
            placeholder="Optional (e.g. Retail, Agriculture)"
        )

        organization_type = st.text_input(
            "Organization Type *",
            placeholder="e.g. Private, Government"
        )

        applicant_income = st.number_input(
            "Applicant Income *",
            min_value=0.0,
            placeholder="Enter anual income"
        )
        
        coapplicant_income = st.number_input(
            "Co-applicant Income",
            min_value=0.0,
            value=0.0
        )

        annual_household_income = st.number_input(
            "Annual Household Income *",
            min_value=0.0,
            value=0.0
        )

        monthly_expense = st.number_input(
            "Monthly Expense *",
            min_value=0.0,
            value=0.0
        )

        asset_value = st.number_input(
            "Asset Value",
            min_value=0.0,
            value=0.0
        )

        existing_emis = st.number_input(
            "Existing EMIs",
            min_value=0.0,
            value=0.0
        )

        loan_amount = st.number_input(
            "Loan Amount *",
            min_value=1000.0,
            max_value=100000000.0,
            value=1000.0
        )

        loan_term_months = st.number_input(
            "Loan Term (Months) *",
            min_value=6,
            max_value=360,
            value=6
        )

        purpose_of_loan = st.text_input(
            "Purpose of Loan *",
            placeholder="e.g. Home Purchase"
        )

        property_area = st.text_input(
            "Property Area *",
            placeholder="e.g. Urban, Rural, Semi-Urban"
        )

        submit = st.form_submit_button("Evaluate", use_container_width=True)

        if submit:

            try:
                validated_data = NewCustomerLoanRequest(
                    customer_name=customer_name,
                    phone_number=phone_number,
                    age=age,
                    gender=gender,
                    married=married,
                    education=education,
                    occupation=occupation,
                    employment_status=employment_status,
                    employment_length_years=employment_length_years,
                    business_type=business_type,
                    organization_type=organization_type,
                    applicant_income=applicant_income,
                    coapplicant_income=coapplicant_income,
                    annual_household_income=annual_household_income,
                    monthly_expense=monthly_expense,
                    asset_value=asset_value,
                    existing_emis=existing_emis,
                    loan_amount=loan_amount,
                    loan_term_months=loan_term_months,
                    purpose_of_loan=purpose_of_loan,
                    property_area=property_area
                )

            except ValidationError as e:
                for error in e.errors():
                    st.error(
                        f"{error['loc'][0]}: {error['msg']}"
                    )
                st.stop()
                
            input_data = validated_data.model_dump()

            input_data.update({
                "is_new_customer": True,
                "cibil_score": 650,
                "credit_history": 0,
                "default_history_count": 0,
                "number_of_previous_loans": 0
            })

            try:
                with st.spinner("Running credit investigation..."):
                    result = engine.evaluate_customer(input_data)

                    customer_id = customer_service.create_new_customer(input_data)
                    loan_id = customer_service.create_loan_application(customer_id, input_data, 
                                                                       result)
                show_result_dashboard(result)

            except Exception as e:
                st.error(f"Evaluation failed: {e}")

st.divider()

st.caption(
    "Credit Risk Investigation Platform | AI + ML + RAG + Multi-Agent System"
)