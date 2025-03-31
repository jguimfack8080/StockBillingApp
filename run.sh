#!/bin/bash

# Créer le répertoire src et les sous-dossiers
mkdir -p src/{app/{services/{sales,stock,payments,reports,auth},core,ui},docker,migrations,tests}

# Créer les fichiers principaux dans chaque dossier
touch src/app/services/sales/{__init__.py,main.py,models.py,schemas.py,crud.py,utils.py}
touch src/app/services/stock/{__init__.py,main.py,models.py,schemas.py,crud.py,utils.py}
touch src/app/services/payments/{__init__.py,main.py,models.py,schemas.py,crud.py,utils.py}
touch src/app/services/reports/{__init__.py,main.py,models.py,schemas.py,crud.py,utils.py}
touch src/app/services/auth/{__init__.py,main.py,models.py,schemas.py,crud.py,utils.py}

touch src/app/core/{__init__.py,config.py,database.py,security.py,dependencies.py,logging.py}
touch src/app/ui/{__init__.py,main_window.py,sales_window.py,stock_window.py,payment_window.py,report_window.py,auth_window.py}

# Créer les fichiers Docker et Docker Compose dans le dossier docker
touch src/docker/{Dockerfile,docker-compose.yml,.env}
touch src/migrations/.empty  # Un fichier pour indiquer que le dossier est vide pour l'instant

# Créer le fichier requirements.txt
touch src/requirements.txt

# Créer le fichier README.md et LICENSE
touch src/README.md src/LICENSE

# Afficher un message de confirmation
echo "La structure du projet a été créée avec succès !"
