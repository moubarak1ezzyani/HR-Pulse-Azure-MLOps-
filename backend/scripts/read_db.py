import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Charger la connexion depuis ton .env
load_dotenv()
DB_URL = os.getenv("DATABASE_URL")

print("🔌 Connexion à Azure SQL...")
engine = create_engine(DB_URL)

# Lire les 10 premières lignes de la table 'jobs' (SQL Server utilise TOP au lieu de LIMIT)
query = "SELECT TOP 10 * FROM jobs"

try:
    df_result = pd.read_sql(query, con=engine)
    print("\n✅ Voici ce qu'il y a dans ta base de données :")
    print(df_result)
except Exception as e:
    print(f"❌ Erreur de lecture : {e}")