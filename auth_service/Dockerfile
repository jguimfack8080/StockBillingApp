FROM python:3.10-slim

WORKDIR /app

ENV PYTHONPATH=/app

COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Copie explicite du fichier .env
COPY .env .env

# Installer netcat-openbsd pour vérifier si MySQL est prêt
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

# Lancer l'application en utilisant un script d'attente (entrypoint.sh)
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

CMD ["/app/entrypoint.sh"]
