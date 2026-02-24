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


## The NLP Cleaning Pipeline
### 1. Normalization (Lowercasing)
We convert all text to lowercase. To a computer, "Python", "PYTHON", and "python" are treated as three distinct words. By normalizing, you reduce the complexity of the vocabulary so the model knows they are the same thing.

### 2. Noise Removal
We remove punctuation, special characters (like #, @, *), and HTML tags if your data was scraped from the web.

Example: "Django!" becomes "Django".

### 3. Stop Words Removal
We remove very frequent words that carry little to no semantic value (e.g., "the", "a", "and", "is", "in").

Impact: This allows the model to focus on high-value keywords like "Cloud", "SQL", or "Developer".

### 4. Lemmatization or Stemming
We reduce words to their root or dictionary form.

Stemming: A "cruder" method that chops off the ends of words (e.g., "connection", "connected", "connective" all become "connect").

Lemmatization: A "smarter" method that uses a dictionary to find the actual root (e.g., "is", "am", "are" all become the lemma "be").

Example: "recruiting", "recruited", and "recruits" all become "recruit".

## increase perfromance
Even if performance isn't the priority for a learning project, understanding **how** to move from a "baseline" to a "high-performing" model is exactly what a Lead Data Scientist or a Recruiter would ask you.

With an $R^2$ of **-0.15**, your model is currently "guessing" worse than just taking the average salary. Here is how you would turn this around in a real-world scenario:

### 1. Better Text Representation (The "NLP" Level)

Currently, you are using **TF-IDF**. It only counts word frequencies. It doesn't understand that "Python" and "Java" are both programming languages.

* **The Fix:** Use **Embeddings**. Instead of TF-IDF, use the vectors you are already generating for ChromaDB (Sentence-Transformers like `all-MiniLM-L6-v2`). These capture the **semantic meaning** of the job description.
* **Feature Extraction:** Use Azure AI Language to extract specific **Skills** (NER). A job that mentions "Cloud Architecture" or "Machine Learning" usually pays more than one that just says "Data Entry."

### 2. Feature Engineering (The "Tabular" Level)

You are currently only using Size and Revenue. Salaries are highly dependent on things you have in your data but aren't using yet:

* **Location:** A "Data Scientist" in San Francisco or Paris earns more than in a small town.
* **Seniority:** Extracting words like "Senior," "Lead," "Junior," or "Intern" from the Job Title is critical.
* **Experience Years:** Use Regex to find numbers followed by "years of experience" in the text. This is often the strongest predictor of salary.

### 3. Upgrade the Algorithm

Random Forest is great, but for tabular data with a mix of text features, modern **Gradient Boosting** algorithms almost always win.

* **The Fix:** Switch to **XGBoost**, **LightGBM**, or **CatBoost**. They are faster and much better at handling the "noise" in your 1000 TF-IDF features.

### 4. Hyperparameter Tuning

You are using the "default" settings of the RandomForest.

* **The Fix:** Use **Optuna** or **GridSearchCV** to find the best number of trees (`n_estimators`), the depth of the trees (`max_depth`), and the number of features to consider.

### 5. Handling Outliers & Scaling

Salaries often have outliers (very high or very low).

* **The Fix:** Check your `Avg_Sal_K` distribution. If it's very skewed, try predicting the **Log of the salary** instead of the raw number. It makes the distribution more "Normal" and easier for the model to learn.

---

### Summary Checklist for a "Version 2":

| Action | Impact |
| --- | --- |
| **Use Sentence Embeddings** | High (Better text understanding) |
| **Extract Seniority (Jr/Sr)** | Very High (Direct salary link) |
| **Switch to XGBoost** | Medium (Better math/optimization) |
| **Add Job Location** | High (Cost of living adjustment) |

**Since you've committed your baseline, would you like to try implementing one of these (like extracting Seniority from the title) or are we ready to move to the API/Azure phase?**