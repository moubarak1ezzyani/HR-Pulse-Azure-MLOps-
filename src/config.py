# Variables globales, chemins
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "df_hr_cleaned.csv")
MODEL_DIR = os.path.join(BASE_DIR, "models")
MODEL_PATH = os.path.join(MODEL_DIR, "saved_models", "salary_predictor.pkl") # régression
EXTRACT_PATH_OUPUT="../data/processed/dataset_with_skills.csv"

#extract skills
ENDPOINT = os.getenv("TON_ENDPOINT")
KEY = os.getenv("TON_KEY")
