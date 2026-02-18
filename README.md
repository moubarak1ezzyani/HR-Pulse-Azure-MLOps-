# HR-Pulse-Azure-MLOps-
End-to-end MLOps solution for job analysis using Azure AI, SQL, and FastAPI. Features automated ETL, salary prediction, Terraform infrastructure, Docker containerization, CI/CD, and OpenTelemetry.

***

## Repository Structure
```plaintext
nlp-ticket-classification/
├── .github/
│   └── workflows/
│       └── ci-pipeline.yml        # CI: Lint & Build Docker (sur push main/develop)
├── data/                          # (IGNORÉ par Git via .gitignore)
│   ├── raw/                       # Dataset original (emails)
│   ├── processed/                 # Données nettoyées
│   └── reference/                 # Baseline pour Evidently
├── docker/
│   ├── Dockerfile.app             # Image pour le pipeline Python
│   └── docker-compose.monitoring.yml # Pour Prometheus/Grafana/Cadvisor (Step 7)
├── k8s/                           # Manifestes Kubernetes (Step 6)
│   ├── cronjob-pipeline.yaml      # Job/CronJob pour le pipeline batch
│   └── ...
├── models/                        # (IGNORÉ par Git ou géré par DVC)
│   ├── classifier.pkl             # Modèle entrainé
│   └── chroma_db/                 # Persistance ChromaDB
├── monitoring/
│   ├── prometheus/
│       └── prometheus.yml         # Config Prometheus (fournie dans le brief)
│   └── grafana/                   # Dashboards exportés (JSON)
├── notebooks/                     # Explorations et POCs
│   ├── 01_eda_preprocessing.ipynb # Étape 1
│   ├── 02_embeddings_chroma.ipynb # Étape 2
│   └── 03_training_eval.ipynb     # Étape 3
├── reports/                       # Sorties générées (IGNORÉ sauf exemples)
│   └── evidently/                 # Rapports HTML Evidently (Step 5)
├── src/                           # Code Source modulaire
│   ├── __init__.py
│   ├── config.py                  # Variables globales, chemins
│   ├── preprocessing.py           # Nettoyage NLP (Step 1)
│   ├── embeddings.py              # HF & ChromaDB (Step 2)
│   ├── train.py                   # Scikit-learn training (Step 3)
│   ├── drift_monitor.py           # Evidently AI script (Step 5)
│   └── main.py                    # Point d'entrée pour lancer le pipeline complet
├── tests/                         # Tests unitaires
├── .gitignore                     # TRES IMPORTANT (voir section 3)
├── README.md                      # Documentation du projet
└── requirements.txt               # Dépendances Python
```

## Les Branches Temporaires (Features)

Pour chaque étape du brief, tu créeras une branche feature/ issue de develop.

    feature/eda-nlp-prep : (Étape 1) Analyse exploratoire, scripts de nettoyage texte.

    feature/embeddings-chromadb : (Étape 2) Intégration Hugging Face et ChromaDB.

    feature/model-training : (Étape 3) Création du modèle sklearn et évaluation.

    feature/ml-monitoring : (Étape 5 - Bonus) Scripts Evidently AI.

    feature/docker-k8s : (Étape 6) Dockerfiles, CI GitHub Actions et Yaml K8s.

    feature/infra-monitoring : (Étape 7) Prometheus, Grafana, Node Exporter.