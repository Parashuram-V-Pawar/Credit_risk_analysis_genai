import pandas as pd


def remove_new_to_credit_customers(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["cibil_score"] != -1].copy()


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    numeric_columns = df.select_dtypes(include=["int64", "float64"]).columns

    categorical_columns = df.select_dtypes(include=["object"]).columns

    for column in numeric_columns:
        df[column] = df[column].fillna(df[column].median())

    for column in categorical_columns:
        df[column] = df[column].fillna("Unknown")

    return df