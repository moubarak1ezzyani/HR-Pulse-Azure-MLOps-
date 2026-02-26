import pandas as pd
import joblib
import os
from config import MODEL_PATH

def predict_salary(description, size_avg, revenue_avg):
    # load model (préprocesseur + RF)
    if not os.path.exists(MODEL_PATH):
        return "Erreur : Le modèle n'a pas été trouvé. Lancez d'abord train.py."
    
    model = joblib.load(MODEL_PATH)
    
    input_data = pd.DataFrame([{
        'cleaned_description': description,
        'Size_Avg': size_avg,
        'Revenue_Avg_Millions': revenue_avg
    }])
    
    
    prediction = model.predict(input_data)
    
    return prediction[0]

if __name__ == "__main__":
    # Test manuel
    print("🔮 Test de prédiction en cours...")
    
    sample_desc = "Looking for a Data Scientist with Python, SQL and Machine Learning experience."
    sample_size = 500  # avg size 
    sample_rev = 100   # avg revenue : milions
    
    salary = predict_salary(sample_desc, sample_size, sample_rev)
    
    print(f"\n📝 Description : {sample_desc}")
    print(f"💰 Salaire prédit : {salary:.2f} K$ / an")