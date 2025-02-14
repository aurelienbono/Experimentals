# Utilisez une image Python officielle et légère
FROM python:3.10-slim

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    chromium-driver \
    chromium \
    && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers nécessaires
COPY requirements.txt .
COPY main.py .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Commande par défaut
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
