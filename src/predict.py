import pandas as pd
import joblib
import os
from config import MODEL_PATH

def predict_salary(description, size_avg, revenue_avg):
    # 1. Charger le modèle (le pipeline complet : préprocesseur + RF)
    if not os.path.exists(MODEL_PATH):
        return "Erreur : Le modèle n'a pas été trouvé. Lancez d'abord train.py."
    
    model = joblib.load(MODEL_PATH)
    
    # 2. Préparer les données d'entrée dans le même format que l'entraînement
    # Le modèle attend les colonnes : 'cleaned_description', 'Size_Avg', 'Revenue_Avg_Millions'
    input_data = pd.DataFrame([{
        'cleaned_description': description,
        'Size_Avg': size_avg,
        'Revenue_Avg_Millions': revenue_avg
    }])
    
    # 3. Faire la prédiction
    prediction = model.predict(input_data)
    
    return prediction[0]

if __name__ == "__main__":
    # Test manuel
    print("🔮 Test de prédiction en cours...")
    
    sample_desc = "Looking for a Data Scientist with Python, SQL and Machine Learning experience."
    sample_size = 500  # Taille moyenne de l'entreprise
    sample_rev = 100   # Revenu moyen en millions
    
    salary = predict_salary(sample_desc, sample_size, sample_rev)
    
    print(f"\n📝 Description : {sample_desc}")
    print(f"💰 Salaire prédit : {salary:.2f} K$ / an")