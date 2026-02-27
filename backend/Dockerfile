# 1. Utiliser une image Python légère
FROM python:3.11-slim

# 2. Installer 'uv' pour une gestion ultra-rapide des dépendances
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 3. Définir le dossier de travail dans le container
WORKDIR /docker

# 4. Copier les fichiers de configuration en premier (optimisation du cache)
COPY pyproject.toml uv.lock ./

# 5. Installer les dépendances sans installer le projet lui-même
RUN uv sync --frozen --no-install-project

# 6. Copier le reste du code (dossiers app, src, models, etc.)
COPY . .

# 7. Exposer le port utilisé par FastAPI
EXPOSE 8000

# 8. Commande pour lancer l'API
# On utilise 'uv run' pour s'assurer que l'environnement virtuel est utilisé
CMD ["uv", "run", "python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]