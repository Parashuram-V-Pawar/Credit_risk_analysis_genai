from sqlalchemy import create_engine
from dotenv import load_dotenv
from urllib.parse import quote_plus
import os

load_dotenv()

username = os.getenv('USERNAME')
password = quote_plus(os.getenv('PASSWORD'))
host = os.getenv('DB_HOST')
port = os.getenv('PORT_NUMBER')
database = os.getenv('DATABASE')


DATABASE_URL = (
    f"mssql+pyodbc://{username}:{password}@{host},{port}/{database}"
    "?driver=ODBC+Driver+18+for+SQL+Server"
    "&TrustServerCertificate=yes")

engine = create_engine(DATABASE_URL)
