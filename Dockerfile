# Utilisez l'image officielle Python comme base
FROM python:3.8-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier le code source de l'application
COPY . /app/

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposez le port de l'application
EXPOSE 8000

# Commande pour démarrer l'application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "analyze_java_django.wsgi:application"]
