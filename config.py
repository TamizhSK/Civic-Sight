import os
from dotenv import load_dotenv

load_dotenv()

# GCP Configuration
GCP_API_KEY = os.getenv("GCP_API_KEY")
PROJECT_ID = os.getenv("PROJECT_ID")
LOCATION = os.getenv("LOCATION", "us")
PROCESSOR_ID = os.getenv("PROCESSOR_ID")

# File paths
PDF_FOLDER = os.getenv("PDF_FOLDER", "data")
OUTPUT_FOLDER = os.getenv("OUTPUT_FOLDER", "output")
OUTPUT_FILE = os.getenv("OUTPUT_FILE", "extracted_data.xlsx")

# Data fields to extract
FIELDS_TO_EXTRACT = [
    "Constituency Name",
    "Total number of electors", 
    "Total number of valid votes polled",
    "Total number of votes for 'None of the Above'"
]