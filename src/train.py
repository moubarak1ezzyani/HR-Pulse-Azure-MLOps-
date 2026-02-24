# Scikit-learn training (Step 3)
import pandas as pd
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from config import BASE_DIR, DATA_PATH, MODEL_DIR, MODEL_PATH

def train_model():
    print("🚀 Démarrage de la phase d'entraînement...")

    # 2. Chargement des données
    df = pd.read_csv(DATA_PATH)
    
    # Nettoyage de sécurité : on supprime les lignes où le salaire (notre cible) est manquant
    df = df.dropna(subset=['Avg_Sal_K'])
    
    # On remplace les NaN éventuels dans le texte par une chaîne vide
    df['cleaned_description'] = df['cleaned_description'].fillna("")

    # 3. Séparation des Features (X) et de la Target (y)
    X = df[['cleaned_description', 'Size_Avg', 'Revenue_Avg_Millions']]
    y = df['Avg_Sal_K']

    # Train / Test split (80% entraînement, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"📊 Données divisées : {len(X_train)} pour l'entraînement, {len(X_test)} pour le test.")

    # 4. Création du Preprocessor avec ColumnTransformer
    # Il applique TF-IDF sur le texte et StandardScaler sur les nombres
    preprocessor = ColumnTransformer(
        transformers=[
            ('text', TfidfVectorizer(max_features=1000), 'cleaned_description'),
            ('num', StandardScaler(), ['Size_Avg', 'Revenue_Avg_Millions'])
        ])

    # 5. Création du Pipeline complet (Préparation + Modèle)
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
    ])

    # 6. Entraînement du modèle
    print("🧠 Entraînement du RandomForest en cours (cela peut prendre quelques secondes)...")
    pipeline.fit(X_train, y_train)

    # 7. Évaluation du modèle
    predictions = pipeline.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    print("\n✅ Évaluation du modèle :")
    print(f"   - MAE (Erreur Absolue Moyenne) : {mae:.2f} K$")
    print(f"   - R² Score (Précision globale) : {r2:.2f}")

    # 8. Sauvegarde du modèle dans le dossier ignoré par Git
    os.makedirs(MODEL_DIR, exist_ok=True) # Crée le dossier s'il n'existe pas
    joblib.dump(pipeline, MODEL_PATH)
    print(f"\n💾 Modèle sauvegardé avec succès dans : {MODEL_PATH}")

if __name__ == "__main__":
    train_model()