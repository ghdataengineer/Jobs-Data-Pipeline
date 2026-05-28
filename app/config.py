from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

# Dates
START_DATE_RAW = os.getenv("START_DATE")
END_DATE_RAW = os.getenv("END_DATE")

if not START_DATE_RAW or not END_DATE_RAW:
    raise ValueError("START_DATE ou END_DATE não definidos no .env")

START_DATE = datetime.strptime(START_DATE_RAW, "%Y-%m-%d").date()
END_DATE = datetime.strptime(END_DATE_RAW, "%Y-%m-%d").date()

# Max jobs
try:
    MAX_JOBS = int(os.getenv("MAX_JOBS", 10))
except ValueError:
    MAX_JOBS = 10

# APIs
API_URLS_RAW = os.getenv("API_URLS", "")
API_URLS = [url.strip() for url in API_URLS_RAW.split(",") if url.strip()]