import pandas as pd
import json
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

# 1. Charger les variables d'environnement
load_dotenv()

DB_URL = os.getenv("DATABASE_URL")
AI_ENDPOINT = os.getenv("TON_ENDPOINT") 
AI_KEY = os.getenv("TON_KEY")           

# 2. Initialiser le client Azure AI
def authenticate_client():
    if not AI_ENDPOINT or not AI_KEY:
        print("⚠️ Clés Azure AI manquantes, l'IA ne sera pas activée (Test local uniquement).")
        return None
    credential = AzureKeyCredential(AI_KEY)
    return TextAnalyticsClient(endpoint=AI_ENDPOINT, credential=credential)

client = authenticate_client()

# 3. Fonction NER (Extraction d'entités)
def extract_skills(description):
    if not client:
        return json.dumps([]) # Retourne une liste vide si pas d'IA
        
    if not isinstance(description, str) or not description.strip():
        return json.dumps([])
    
    try:
        # Azure limite à 5120 caractères par requête, on coupe par sécurité
        doc = [description[:5000]]
        response = client.recognize_entities(documents=doc)[0]
        
        skills = []
        for entity in response.entities:
            # On cible la catégorie 'Skill' (Compétence) identifiée par Azure
            if entity.category == "Skill":
                skills.append(entity.text)
        
        # On dédoublonne avec set() et on convertit en JSON
        return json.dumps(list(set(skills)))
        
    except Exception as e:
        print(f"❌ Erreur IA sur une ligne : {e}")
        return json.dumps([])

# 4. Pipeline principal
def main():
    print("📥 1. Chargement des données nettoyées...")
    
    script_dir = os.path.dirname(os.path.abspath(__file__)) 
    clean_file_path = os.path.join(script_dir, "../data/processed/df_hr_cleaned.csv")
    
    
    # clean_file_path ="../data/processed/df_hr_cleaned.csv"
    try:
        df = pd.read_csv(clean_file_path)
    except FileNotFoundError:
        print(f"❌ Fichier introuvable au chemin : {clean_file_path}")
        return

    print("🧹 2. Préparation des colonnes pour la base de données...")
    
    # 'Job Title' -> 'job_title' & 'index' -> 'id'
    df = df.rename(columns={
        'Job Title': 'job_title',
        'index': 'id'
    })

    # col id n'a pas pu être créée à partir de l'index -> génèrée
    if 'id' not in df.columns:
        df['id'] = range(1, len(df) + 1)

    # 🛑 SÉCURITÉ : On teste sur 5 lignes seulement pour économiser Azure !
    df_sample = df.head(5).copy()

    print("🧠 3. Extraction des compétences (NER) sur 'Job Description'...")
    # On utilise bien le texte d'origine pour l'IA, pas le cleaned_description
    df_sample['skills_extracted'] = df_sample['Job Description'].apply(extract_skills)

    # On ne garde que les 3 colonnes demandées par le brief
    df_final = df_sample[['id', 'job_title', 'skills_extracted']]
    print("\nAperçu des données à envoyer :")
    print(df_final.head())

    print("\n💾 4. Injection dans Azure SQL...")
    try:
        engine = create_engine(DB_URL)
        # Injection dans une table nommée 'jobs'
        df_final.to_sql('jobs', con=engine, if_exists='replace', index=False)
        print("✅ Données injectées avec succès dans ta base de données Azure SQL !")
    except Exception as e:
        print(f"❌ Erreur de connexion SQL : {e}")

if __name__ == "__main__":
    main()