import streamlit as st
import pandas as pd

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
st.title("🏦 Credit Risk Investigation Platform")
st.caption(
    "AI-Powered Loan Approval, Risk Assessment & Investigation"
)

st.set_page_config(
    page_title="Credit Risk Investigation",
    page_icon="🏦",
    layout="wide"
)
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
        st.success(f"✅ FINAL DECISION: {decision}")
    elif decision == "CONDITIONAL_APPROVAL":
        st.warning(f"⚠️ FINAL DECISION: {decision}")
    else:
        st.error(f"❌ FINAL DECISION: {decision}")
    st.divider()

    tab1, tab2, tab3, tab4 = st.tabs([
        "Approval Analysis",
        "Risk Analysis",
        "History Analysis",
        "Final Report"
    ])

    with tab1:
        st.write(result["approval_analysis"])
    with tab2:
        st.write(result["risk_analysis"])
    with tab3:
        st.write(result["history_analysis"])
    with tab4:
        st.markdown(result["final_report"])

    if result.get("similar_cases"):
        st.divider()
        st.subheader("📚 Similar Historical Cases")

        for idx, case in enumerate(
            result["similar_cases"],
            start=1
        ):
            with st.expander(f"Case {idx}"):
                st.text(case)

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

            show_result_dashboard(result)

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

                show_result_dashboard(result)

            except Exception as e:
                st.error(f"Evaluation failed: {e}")