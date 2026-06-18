from sqlalchemy import create_engine
from dotenv import load_dotenv
from urllib.parse import quote_plus
import os

load_dotenv()

username = os.getenv("USERNAME")
password_raw = os.getenv("PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("PORT_NUMBER")
database = os.getenv("DATABASE")

# =========================
# SAFE CHECK (IMPORTANT FIX)
# =========================
if not password_raw:
    raise ValueError("PASSWORD is missing in .env file")

password = quote_plus(password_raw)

DATABASE_URL = (
    f"mssql+pyodbc://{username}:{password}@{host},{port}/{database}"
    "?driver=ODBC+Driver+18+for+SQL+Server"
    "&TrustServerCertificate=yes"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)