#!/bin/bash

# Attendre que MySQL soit prêt
until nc -z -v -w30 mysql 3306
do
  echo "En attente de MySQL..."
  sleep 1
done

# Démarrer l'application avec uvicorn
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
