FROM python:3.11-slim

# Installer dépendances système
RUN apt-get update && apt-get install -y \
    build-essential libpq-dev curl \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Créer répertoire de l’app
WORKDIR /app

# Installer requirements
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copier le projet
COPY . /app/

# Initialiser tailwind
RUN python manage.py tailwind install \
    && python manage.py tailwind build

# Collecter les fichiers statiques
RUN python manage.py collectstatic --noinput

# Commande par défaut : lancer Gunicorn
CMD ["gunicorn", "main.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
