# Utiliser une image de base officielle Python
FROM python:3.11-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers du projet dans le conteneur
COPY . /app

# Installer les dépendances nécessaires
RUN pip install --no-cache-dir requests beautifulsoup4

# Définir la commande à exécuter lorsque le conteneur démarre
CMD ["python", "main.py"]
