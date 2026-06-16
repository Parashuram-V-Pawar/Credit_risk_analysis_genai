import pandas as pd

def clean_customers_data(df: pd.DataFrame) -> pd.DataFrame:
    # Remove leading/trailing spaces
    df = df.apply(
        lambda col: col.str.strip()
        if col.dtype == "object"
        else col
    )

    df.columns = (
        df.columns
        .str.strip()
    )

    # Convert Aadhaar & Phone to string
    df["Aadhaar_Synthetic"] = (
        df["Aadhaar_Synthetic"]
        .astype(str)
        .str.replace(".0", "", regex=False)
    )

    df["Phone_Number"] = (
        df["Phone_Number"]
        .astype(str)
        .str.replace(".0", "", regex=False)
    )

    # Standardize Emails
    df["Email"] = (
        df["Email"]
        .astype(str)
        .str.lower()
        .str.strip()
    )

    # Standardize names
    df["Customer_Name"] = (
        df["Customer_Name"]
        .astype(str)
        .str.title()
    )

    # Remove completely empty rows
    df.dropna(how="all", inplace=True)

    # Remove duplicate Aadhaar
    df.drop_duplicates(
        subset=["Aadhaar_Synthetic"],
        keep="first",
        inplace=True
    )

    # # Remove duplicate Emails
    # df.drop_duplicates(
    #     subset=["Email"],
    #     keep="first",
    #     inplace=True
    # )

    # Remove records with missing mandatory fields
    mandatory_cols = [
        "Customer_Name",
        "Aadhaar_Synthetic",
        "Phone_Number",
        "Email"
    ]

    df.dropna(
        subset=mandatory_cols,
        inplace=True
    )

    # Age cleaning
    df["Age"] = pd.to_numeric(
        df["Age"],
        errors="coerce"
    )

    df = df[
        (df["Age"] >= 18) &
        (df["Age"] <= 80)
    ]

    # # Remove invalid phone numbers
    # df = df[
    #     df["Phone_Number"]
    #     .str.match(r"^[6-9]\d{9}$", na=False)
    # ]

    # Remove invalid Aadhaar
    df = df[
        df["Aadhaar_Synthetic"]
        .str.match(r"^\d{12}$", na=False)
    ]

    # Remove invalid PIN codes
    df["PIN_Code"] = df["PIN_Code"].astype(str)

    df = df[
        df["PIN_Code"]
        .str.match(r"^\d{6}$", na=False)
    ]

    return df.reset_index(drop=True)