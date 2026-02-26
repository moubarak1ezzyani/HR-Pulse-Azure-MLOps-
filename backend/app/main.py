from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import joblib
import pandas as pd
import os

app = FastAPI(
    title="HR Pulse API",
    description="API de prédiction pour les ressources humaines",
    version="1.0.0"
)

# link to the frontend part
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # Autorise uniquement ton Frontend Next.js local
    allow_credentials=True,
    allow_methods=["*"], # Autorise toutes les méthodes (GET, POST, etc.)
    allow_headers=["*"], # Autorise tous les headers
)


# 2. Charger le modèle ML (Random Forest)
try:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    MODEL_DIR = os.path.join(BASE_DIR, "models")
    MODEL_PATH = os.path.join(MODEL_DIR, "saved_models", "salary_predictor.pkl") # régression
    model = joblib.load(MODEL_PATH)
    print("✅ Modèle ML chargé avec succès !")
except FileNotFoundError:
    model = None
    print(f"⚠️ Attention : Modèle introuvable au chemin {MODEL_PATH}.")

# 3. Définir le format des données attendues en entrée
# ⚠️ Adapte ces variables selon les features exactes de ton modèle Random Forest
class EmployeeData(BaseModel):
    cleaned_description: str = Field(..., description="La description nettoyée du poste")
    Size_Avg: float = Field(..., description="La taille moyenne de l'entreprise (en nombre d'employés)")
    Revenue_Avg_Millions: float = Field(..., description="Le revenu moyen de l'entreprise en millions")

# 4. Route de test (pour voir si l'API est réveillée)
@app.get("/")
def home():
    return {"message": "Bienvenue sur l'API HR Pulse ! 🚀"}

# 5. Route de prédiction
@app.post("/predict")
def predict(data: EmployeeData):
    # Sécurité si le modèle n'a pas chargé
    if model is None:
        raise HTTPException(status_code=500, detail="Modèle ML non disponible sur le serveur.")
    
    try:
        # On transforme le JSON reçu en DataFrame d'une seule ligne
        input_data = pd.DataFrame([data.model_dump()])
        
        # On fait la prédiction avec le modèle
        prediction = model.predict(input_data)
        
        # On renvoie le résultat (on convertit en float ou int pour que JSON comprenne)
        return {"prediction": float(prediction[0])}
        
    except Exception as e:
        # S'il manque une colonne ou que le format est mauvais
        raise HTTPException(status_code=400, detail=f"Erreur de prédiction : {str(e)}")