import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

DB_PATH = "db"
TABLE_NAME = "documents"
DOCUMENTS_PATH = "data/documents"