import pandas as pd
import logging

from src.database.data_insertion import *

logging.basicConfig(level=logging.INFO)

def load_data():
    logging.info("Inserting data into database...")

    logging.info("Loading data")
    df = pd.read_csv("./dataset/HDFC_CreditRisk_10000_Customers.csv")
    logging.info("Data loaded")

    try:
        logging.info("Inserting customer data...")
        customer_insert(df)
        logging.info("Customer data inserted successfully...")

        logging.info("Inserting employment profile data...")
        employment_profiles_insert(df)
        logging.info("employment profile data inserted successfully...")

        logging.info("Inserting financial profile data...")
        financial_profiles_insert(df)
        logging.info("financial profile data inserted successfully...")

        logging.info("Inserting credit profile data...")
        credit_profiles_insert(df)
        logging.info("credit profile data inserted successfully...")

        logging.info("Inserting loan application data...")
        loan_applications_insert(df)
        logging.info("loan application data inserted successfully...")

        logging.info("Data insertion completed...")

    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    load_data()