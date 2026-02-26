# Evidently AI script (Step 5)
import os
import pandas as pd
import ast
import joblib
from sklearn.model_selection import train_test_split

# Importations spécifiques à Evidently AI
from evidently import Report
from evidently.presets import RegressionPreset, DataDriftPreset

print("📊 Lancement de l'évaluation du modèle avec Evidently AI...")

# 1. Créer le dossier pour ranger les rapports HTML
os.makedirs("../reports", exist_ok=True)

# 2. Charger les données (comme dans le script d'entraînement)
df_main = pd.read_csv("../../data/processed/df_hr_cleaned.csv")
df_skills = pd.read_csv("../../data/processed/extracted_skills_only.csv")
df = pd.concat([df_main, df_skills], axis=1).dropna(subset=['Avg_Sal_K'])

def parse_skills(skill_string):
    try:
        return ast.literal_eval(skill_string)
    except:
        return []

df['extracted_skills'] = df['extracted_skills'].apply(parse_skills)

# 3. Charger le modèle et le binariseur déjà entraînés !
rf_model = joblib.load("../../models/rf_skills_model.pkl")
mlb = joblib.load("../../models/skills_binarizer.pkl")

# Transformation des compétences
skills_encoded = mlb.transform(df['extracted_skills'])
skills_df = pd.DataFrame(skills_encoded, columns=mlb.classes_, index=df.index)

# Préparation X et y
X = pd.concat([df[['Size_Avg', 'Revenue_Avg_Millions']], skills_df], axis=1)
y = df['Avg_Sal_K']

# Séparation (On doit utiliser le même random_state=42 pour retrouver les mêmes données)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Préparer les DataFrames pour Evidently
# Evidently a besoin que la cible s'appelle 'target' et la prédiction 'prediction'
print("🧠 Calcul des prédictions pour le rapport...")

# Données de Référence (Entraînement)
reference_data = X_train.copy()
reference_data['target'] = y_train
reference_data['prediction'] = rf_model.predict(X_train)

# Données Actuelles (Test)
current_data = X_test.copy()
current_data['target'] = y_test
current_data['prediction'] = rf_model.predict(X_test)

# 5. Création et génération du rapport Evidently
print("📈 Génération du rapport de performance de Régression...")
regression_report = Report(metrics=[
    RegressionPreset(), # Analyse complète des erreurs (MAE, RMSE, R2, etc.)
    DataDriftPreset()   # Vérifie si les données de test sont trop différentes de l'entraînement
])

regression_report.run(reference_data=reference_data, current_data=current_data)

# 6. Sauvegarde en fichier HTML
report_path = "../reports/model_evaluation_report.html"
regression_report.save_html(report_path)

print(f"✅ Rapport généré avec succès ! Ouvre le fichier '{report_path}' dans ton navigateur web.")
