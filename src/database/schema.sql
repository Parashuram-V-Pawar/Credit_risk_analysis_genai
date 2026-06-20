-- Stores the customer's identity information.
CREATE TABLE customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    customer_name VARCHAR(150),
    aadhaar_synthetic VARCHAR(20) UNIQUE,
    phone_number VARCHAR(20),
    email VARCHAR(150),
    gender VARCHAR(20),
    age INT,
    religion VARCHAR(50),
    married VARCHAR(20),
    dependents INT,
    education VARCHAR(100),
    occupation VARCHAR(100),
    state VARCHAR(100),
    city VARCHAR(100),
    pin_code VARCHAR(20),
    created_at DATETIME DEFAULT GETDATE()
);
GO 

-- Stores customer's employment-related information.
CREATE TABLE employment_profiles (
    employment_profile_id INT IDENTITY(1,1) PRIMARY KEY,
    customer_id VARCHAR(50),
    employment_status VARCHAR(50),
    employment_length_years INT,
    business_type VARCHAR(100),
    organization_type VARCHAR(100),
    FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
);
GO

-- Stores customer's income and expense information.
CREATE TABLE financial_profiles (
    financial_profile_id INT IDENTITY(1,1) PRIMARY KEY,
    customer_id VARCHAR(50),
    applicant_income FLOAT,
    coapplicant_income FLOAT,
    annual_household_income FLOAT,
    monthly_expense FLOAT,
    asset_value FLOAT,
    existing_emis FLOAT,
    debt_to_income_ratio FLOAT,
    FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
);
GO

-- Stores customer's credit history.
CREATE TABLE credit_profiles (
    credit_profile_id INT IDENTITY(1,1) PRIMARY KEY,
    customer_id VARCHAR(50),
    cibil_score INT,
    credit_history INT,
    default_history_count INT,
    number_of_previous_loans INT,
    FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
);
GO

-- Stores every loan application.
CREATE TABLE loan_applications (
    loan_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50),
    bank_name VARCHAR(100),
    loan_amount FLOAT,
    loan_term_months INT,
    purpose_of_loan VARCHAR(100),
    property_area VARCHAR(50),
    guarantor VARCHAR(100),
    cosigner_relationship VARCHAR(100),
    loan_status VARCHAR(50),
    application_date DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
);
GO

SELECT * FROM customers WHERE phone_number = '7019883440';


CREATE UNIQUE INDEX UX_aadhaar_synthetic
ON customers(aadhaar_synthetic)
WHERE aadhaar_synthetic IS NOT NULL;