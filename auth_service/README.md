# Service d'Authentification (Auth Service)

Ce service gère l'authentification et la gestion des utilisateurs pour l'application de gestion de stock et de facturation.

## Fonctionnalités Principales

### 1. Gestion des Utilisateurs
- Création de comptes utilisateurs
- Gestion des rôles (admin, manager, cashier)
- Désactivation/réactivation des comptes
- Suivi des informations utilisateurs

### 2. Authentification
- Génération de tokens JWT
- Validation des identifiants
- Protection contre l'accès des comptes désactivés
- Gestion des sessions

### 3. Sécurité
- Hachage des mots de passe avec bcrypt
- Tokens JWT sécurisés
- Vérification des privilèges d'administrateur
- Protection des routes sensibles

## Structure de la Base de Données

### Table `users`
- `id`: Identifiant unique
- `first_name`: Prénom
- `last_name`: Nom
- `birth_date`: Date de naissance
- `id_card_number`: Numéro de carte d'identité
- `email`: Adresse email (unique)
- `hashed_password`: Mot de passe haché
- `role`: Rôle de l'utilisateur (admin/manager/cashier)
- `is_active`: Statut du compte
- `created_at`: Date de création
- `deactivation_date`: Date de désactivation
- `deactivation_reason`: Raison de la désactivation

## API Endpoints

### Authentification

#### Obtenir un token
```bash
curl -X POST "http://localhost:8001/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=password"
```

### Gestion des Utilisateurs

#### Créer un utilisateur (Admin uniquement)
```bash
curl -X POST "http://localhost:8001/users/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "birth_date": "1990-01-01",
    "id_card_number": "123456789",
    "email": "john.doe@example.com",
    "password": "password123",
    "role": "cashier"
  }'
```

#### Lister tous les utilisateurs (Admin uniquement)
```bash
curl -X GET "http://localhost:8001/users/" \
  -H "Authorization: Bearer $TOKEN"
```

#### Désactiver/Réactiver un utilisateur (Admin uniquement)
```bash
curl -X PUT "http://localhost:8001/users/deactivate/1" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"reason": "Inactive account"}'
```

#### Récupérer ses propres informations
```bash
curl -X GET "http://localhost:8001/users/me" \
  -H "Authorization: Bearer $TOKEN"
```

## Rôles et Permissions

### Admin
- Créer des utilisateurs
- Lister tous les utilisateurs
- Désactiver/Réactiver des comptes
- Accès à toutes les fonctionnalités

### Manager
- Accès aux fonctionnalités de gestion
- Pas d'accès à la gestion des utilisateurs

### Cashier
- Accès aux fonctionnalités de caisse
- Pas d'accès à la gestion

## Sécurité

### Protection des Comptes
- Les comptes désactivés ne peuvent pas s'authentifier
- Les mots de passe sont hachés avec bcrypt
- Les tokens JWT expirent après un certain temps
- Validation des rôles pour chaque endpoint

### Validation des Données
- Vérification de l'unicité des emails
- Vérification de l'unicité des numéros de carte d'identité
- Validation des dates de naissance
- Validation des rôles

## Configuration

Le service utilise les variables d'environnement suivantes :
- `AUTH_SERVICE_URL`: URL du service d'authentification
- `SECRET_KEY`: Clé secrète pour les tokens JWT
- `ALGORITHM`: Algorithme de chiffrement (HS256 par défaut)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Durée de validité des tokens

## Démarrage

1. Installer les dépendances :
```bash
pip install -r requirements.txt
```

2. Configurer les variables d'environnement

3. Lancer le service :
```bash
uvicorn app.main:app --reload
```

## Tests

Des scripts de test sont disponibles dans le dossier `testscript/` :
- `auth.sh`: Tests d'authentification
- `auth_service.sh`: Tests du service complet 