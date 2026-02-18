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


## UV : venv alternative
### Core Commands (The uv Workflow)

|Action | Old Way (pip) |New Way (uv)
|:---:|:---:|:---:|
Install a package|`pip install pandas`|`uv add pandas`
Create environment|`python -m venv .venv`|`uv venv`
Sync environment|`pip install -r reqs.txt`|`uv sync`
Run a script|`python main.py`|`uv run main.py`

***
## UV setup
### 1. The "Fresh" Installation

Run this in a fresh PowerShell window (as an administrator if possible):

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

```

**CRITICAL:** Restart your terminal or run `$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")` to make the `uv` command available.

---

### 2. The `uv` Workflow (Step-by-Step)

Instead of the old `python -m venv` and `pip install`, follow this sequence inside your project folder:

#### A. Initialize the Project

This creates the `pyproject.toml` which is mandatory for `uv` to track your "background."

```powershell
uv init

```

#### B. Pick your Python Version

One of `uv`'s best features is that it can download Python for you if you don't have the right version.

```powershell
uv python pin 3.11

```

#### C. Install & Create Environment

When you add your first package, `uv` automatically creates a `.venv` folder for you. It uses a **global cache**, so if you delete the folder and reinstall, it takes 0.5 seconds.

```powershell
uv add transformers datasets scikit-learn chromadb evidently prometheus-client pandas numpy

```

*Note: This creates the `uv.lock` file. **Never edit this file manually.** It is your "reproducibility insurance" for Kubernetes.*

---

### 3. Using the Environment

You have two ways to work with this "background" venv:

* **The "Transparent" Way (Recommended):** Just prefix your commands with `uv run`.
* Example: `uv run python src/main.py`.
* *Why?* `uv` will check if your `pyproject.toml` changed and update the venv automatically before running.


* **The "Old School" Way:** You can still activate it if you prefer:
```powershell
.venv\Scripts\activate

```



---

### 4. Setup for VS Code

Since you are likely using VS Code:

1. Open your project.
2. Press `Ctrl + Shift + P`.
3. Type **"Python: Select Interpreter"**.
4. Choose the one inside your `.venv` folder (it should be labeled `('venv': uv)`).

---

### 5. Summary Table for your Workflow

| Goal | Command |
| --- | --- |
| **Reset everything** | Delete `.venv` and `uv.lock`, then run `uv sync` |
| **Add a new tool** | `uv add <package_name>` |
| **Run your NLP script** | `uv run python src/main.py` |
| **Check dependencies** | `uv tree` (Very cool for debugging) |

### Next Step

Now that `uv` is set up, would you like me to create the **`pyproject.toml`** content specifically for your brief's NLP requirements (including the Hugging Face and ChromaDB versions)?


|Feature|Old Way (pip)|New Way (uv)|
|:---:|:---:|:---:|
|Main Config|`requirements.txt`|`pyproject.toml`|
|Exact Versioning|`pip freeze > reqs.txt`|`uv.lock` (Auto-generated)|
|Environment Sync|`pip install -r ...`|`uv sync`|