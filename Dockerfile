# Étape 1 : Choisir l'image de base
FROM python:3.11-slim

# Étape 2 : Empêcher Python de créer des fichiers .pyc
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Étape 3 : Installer les dépendances système
RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Étape 4 : Définir le répertoire de travail
WORKDIR /app

# Étape 5 : Installer les dépendances Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Étape 6 : Copier le code du projet
COPY . /app/

# Étape 7 : Commande par défaut (modifiable via docker-compose)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "mon_projet.wsgi:application"]
