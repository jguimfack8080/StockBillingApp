# Service de Vente (Sales Service)

Ce service gère toutes les opérations liées aux ventes, aux clients et aux transactions dans le système de gestion de stock et de facturation.

## Fonctionnalités Principales

### 1. Gestion des Clients
- Création, lecture, mise à jour et suppression des clients
- Gestion des informations client (nom, prénom, email, téléphone, adresse)
- Historique des ventes par client

### 2. Gestion des Ventes
- Création de ventes avec numéros uniques
- Gestion des articles de vente
- Calcul automatique des totaux
- Gestion des méthodes de paiement
- Notes et commentaires sur les ventes

### 3. Gestion des Transactions
- Enregistrement des paiements
- Calcul automatique de la monnaie
- Gestion des différents modes de paiement (espèces, carte, virement)
- Suivi du statut des transactions

## Structure de la Base de Données

### Tables Principales
1. `customers`
   - Informations des clients
   - Historique des achats
   - Coordonnées de contact

2. `sales`
   - Numéro de vente unique
   - Informations sur le caissier
   - Client associé
   - Montant total
   - Méthode de paiement
   - Statut de la vente

3. `sale_items`
   - Articles vendus
   - Quantités
   - Prix unitaires
   - Totaux par article

4. `transactions`
   - Paiements effectués
   - Montants reçus
   - Monnaie rendue
   - Statut des transactions

## API Endpoints

### Clients

#### Créer un client
```bash
curl -X POST "http://localhost:8002/customers/" \
-H "Content-Type: application/json" \
-d '{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "phone": "+1234567890",
  "address": "123 Main St"
}'
```

#### Lister tous les clients
```bash
curl -X GET "http://localhost:8002/customers/" \
-H "Content-Type: application/json"
```

#### Récupérer un client par ID
```bash
curl -X GET "http://localhost:8002/customers/1" \
-H "Content-Type: application/json"
```

#### Mettre à jour un client
```bash
curl -X PUT "http://localhost:8002/customers/1" \
-H "Content-Type: application/json" \
-d '{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe.updated@example.com",
  "phone": "+1234567890",
  "address": "456 New St"
}'
```

#### Supprimer un client
```bash
curl -X DELETE "http://localhost:8002/customers/1" \
-H "Content-Type: application/json"
```

### Ventes

#### Créer une vente simple
```bash
curl -X POST "http://localhost:8002/sales/" \
-H "Content-Type: application/json" \
-d '{
  "cashier_id": 1,
  "customer_id": 1,
  "payment_method": "CASH",
  "items": [
    {
      "product_id": 1,
      "quantity": 2,
      "unit_price": 20.0
    }
  ],
  "transactions": [
    {
      "amount": 40.0,
      "payment_method": "CASH",
      "amount_received": 50.0
    }
  ],
  "notes": "Vente simple"
}'
```

#### Créer une vente avec plusieurs produits
```bash
curl -X POST "http://localhost:8002/sales/" \
-H "Content-Type: application/json" \
-d '{
  "cashier_id": 1,
  "customer_id": 1,
  "payment_method": "CASH",
  "items": [
    {
      "product_id": 1,
      "quantity": 2,
      "unit_price": 20.0
    },
    {
      "product_id": 2,
      "quantity": 1,
      "unit_price": 50.0
    }
  ],
  "transactions": [
    {
      "amount": 90.0,
      "payment_method": "CASH",
      "amount_received": 100.0
    }
  ],
  "notes": "Vente multiple produits"
}'
```

#### Créer une vente avec paiement mixte (partie carte, partie espèces)
```bash
curl -X POST "http://localhost:8002/sales/" \
-H "Content-Type: application/json" \
-d '{
  "cashier_id": 1,
  "customer_id": 1,
  "payment_method": "MIXED",
  "items": [
    {
      "product_id": 1,
      "quantity": 2,
      "unit_price": 50.0
    }
  ],
  "transactions": [
    {
      "amount": 50.0,
      "payment_method": "CARD",
      "payment_details": "1234-5678-9012-3456"
    },
    {
      "amount": 50.0,
      "payment_method": "CASH",
      "amount_received": 60.0
    }
  ],
  "notes": "Paiement mixte : 50€ par carte, 50€ en espèces"
}'
```

#### Créer une vente sans client
```bash
curl -X POST "http://localhost:8002/sales/" \
-H "Content-Type: application/json" \
-d '{
  "cashier_id": 1,
  "payment_method": "CASH",
  "items": [
    {
      "product_id": 1,
      "quantity": 2,
      "unit_price": 20.0
    },
    {
      "product_id": 2,
      "quantity": 1,
      "unit_price": 50.0
    }
  ],
  "transactions": [
    {
      "amount": 90.0,
      "payment_method": "CASH",
      "amount_received": 100.0
    }
  ],
  "notes": "Vente sans client"
}'
```

#### Lister toutes les ventes
```bash
curl -X GET "http://localhost:8002/sales/" \
-H "Content-Type: application/json"
```

#### Récupérer une vente par ID
```bash
curl -X GET "http://localhost:8002/sales/1" \
-H "Content-Type: application/json"
```

#### Récupérer une vente par numéro
```bash
curl -X GET "http://localhost:8002/sales/number/V20240411-00001" \
-H "Content-Type: application/json"
```

#### Mettre à jour une vente
```bash
curl -X PUT "http://localhost:8002/sales/1" \
-H "Content-Type: application/json" \
-d '{
  "status": "COMPLETED",
  "payment_method": "CARD",
  "notes": "Mise à jour de la vente"
}'
```

### Transactions

#### Créer une transaction
```bash
curl -X POST "http://localhost:8002/transactions/" \
-H "Content-Type: application/json" \
-d '{
  "sale_id": 1,
  "amount": 100.0,
  "payment_method": "CASH",
  "amount_received": 120.0,
  "payment_details": null
}'
```

#### Lister toutes les transactions
```bash
curl -X GET "http://localhost:8002/transactions/" \
-H "Content-Type: application/json"
```

#### Récupérer une transaction par ID
```bash
curl -X GET "http://localhost:8002/transactions/1" \
-H "Content-Type: application/json"
```

#### Mettre à jour une transaction
```bash
curl -X PUT "http://localhost:8002/transactions/1" \
-H "Content-Type: application/json" \
-d '{
  "status": "COMPLETED",
  "payment_details": "1234-5678-9012-3456"
}'
```

## Codes de Réponse HTTP

- `200 OK` : Requête réussie
- `201 Created` : Ressource créée avec succès
- `204 No Content` : Requête réussie mais pas de contenu à retourner
- `400 Bad Request` : Requête mal formulée
- `404 Not Found` : Ressource non trouvée
- `422 Unprocessable Entity` : Erreur de validation des données
- `500 Internal Server Error` : Erreur serveur

## Fonctionnalités Avancées

### 1. Numéros de Vente Uniques
- Format : `VYYYYMMDD-XXXXX`
- Génération automatique
- Garantie d'unicité

### 2. Calculs Automatiques
- Total de la vente
- Monnaie à rendre
- Totaux par article
- Validation des montants

### 3. Gestion des Paiements
- Paiement en espèces
- Paiement par carte
- Paiement par virement
- Paiements mixtes

### 4. Relations Client-Vente
- Historique des achats
- Informations de facturation
- Suivi des préférences

## Notes d'Utilisation Importantes

1. **Création de Vente**
   - Le numéro de vente est généré automatiquement
   - Le total est calculé automatiquement
   - Les transactions sont validées

2. **Gestion des Clients**
   - Les informations client sont optionnelles
   - L'historique des achats est maintenu
   - Les coordonnées peuvent être mises à jour

3. **Transactions**
   - Le statut est suivi automatiquement
   - La monnaie est calculée pour les paiements en espèces
   - Les détails de paiement sont sécurisés

4. **Sécurité**
   - Validation des données
   - Gestion des erreurs
   - Traçabilité des opérations

## Configuration

Le service nécessite les variables d'environnement suivantes :
- `DATABASE_URL` : URL de connexion à la base de données
- `AUTH_SERVICE_URL` : URL du service d'authentification

## Dépendances

- FastAPI
- SQLAlchemy
- Pydantic
- PyMySQL
- Python 3.10+

## Tests des Endpoints

### 1. Créer une Vente
```bash
curl -X POST "http://localhost:8002/sales/" \
-H "Content-Type: application/json" \
-d '{
  "cashier_id": 1,
  "total_amount": 21.98,
  "payment_method": "cash",
  "items": [
    {
      "product_id": 1,
      "quantity": 2,
      "unit_price": 10.99
    }
  ],
  "transactions": [
    {
      "amount": 21.98,
      "payment_method": "cash"
    }
  ]
}'
```

### 2. Lister les Ventes
```bash
curl "http://localhost:8002/sales/"
```

### 3. Obtenir une Vente Spécifique
```bash
curl "http://localhost:8002/sales/1"
```

### 4. Mettre à Jour une Vente
```bash
curl -X PUT "http://localhost:8002/sales/1" \
-H "Content-Type: application/json" \
-d '{
  "status": "completed",
  "payment_method": "card"
}'
```

## Dépendances

Les principales dépendances du service sont :
- FastAPI : Framework web
- SQLAlchemy : ORM pour la base de données
- Pydantic : Validation des données
- PyMySQL : Driver MySQL
- python-dotenv : Gestion des variables d'environnement

## Installation

1. Cloner le dépôt
2. Installer les dépendances :
```bash
pip install -r requirements.txt
```
3. Configurer les variables d'environnement
4. Démarrer le service :
```bash
uvicorn main:app --host 0.0.0.0 --port 8002
```

## Intégration avec Docker

Le service est configuré pour fonctionner dans un conteneur Docker. Pour le démarrer :

```bash
docker-compose up sales_service
```

## Sécurité

- Le service vérifie l'authenticité des caissiers via le service d'authentification
- Les transactions sont enregistrées avec leur statut pour le suivi
- Les montants sont validés pour éviter les erreurs de calcul

## Logs et Monitoring

Les logs du service incluent :
- Création de nouvelles ventes
- Mises à jour de statut
- Erreurs de validation
- Problèmes de connexion à la base de données

## Support et Maintenance

Pour signaler un problème ou demander de l'aide :
1. Vérifier les logs du service
2. S'assurer que la base de données est accessible
3. Vérifier la connexion avec le service d'authentification
4. Contacter l'équipe de support si nécessaire

## Requêtes Curl Complètes

### 1. Créer une Vente
```bash
curl -X POST "http://localhost:8002/sales/" \
-H "Content-Type: application/json" \
-d '{
  "cashier_id": 1,
  "total_amount": 21.98,
  "payment_method": "cash",
  "items": [
    {
      "product_id": 1,
      "quantity": 2,
      "unit_price": 10.99
    }
  ],
  "transactions": [
    {
      "amount": 21.98,
      "payment_method": "cash"
    }
  ]
}'
```

### 2. Lister les Ventes
```bash
# Récupérer toutes les ventes
curl "http://localhost:8002/sales/"

# Récupérer les ventes avec pagination
curl "http://localhost:8002/sales/?skip=0&limit=10"

# Récupérer les ventes avec un offset
curl "http://localhost:8002/sales/?skip=10&limit=20"
```

### 3. Obtenir une Vente Spécifique
```bash
# Récupérer une vente par son ID
curl "http://localhost:8002/sales/1"
```

### 4. Mettre à Jour une Vente
```bash
# Mettre à jour le statut d'une vente
curl -X PUT "http://localhost:8002/sales/1" \
-H "Content-Type: application/json" \
-d '{
  "status": "completed"
}'

# Mettre à jour la méthode de paiement
curl -X PUT "http://localhost:8002/sales/1" \
-H "Content-Type: application/json" \
-d '{
  "payment_method": "card"
}'

# Mettre à jour le statut et la méthode de paiement
curl -X PUT "http://localhost:8002/sales/1" \
-H "Content-Type: application/json" \
-d '{
  "status": "completed",
  "payment_method": "card"
}'
```

### 5. Exemples de Requêtes avec Différentes Méthodes de Paiement

#### Paiement en Espèces
```bash
curl -X POST "http://localhost:8002/sales/" \
-H "Content-Type: application/json" \
-d '{
  "cashier_id": 1,
  "total_amount": 50.00,
  "payment_method": "cash",
  "items": [
    {
      "product_id": 1,
      "quantity": 1,
      "unit_price": 50.00
    }
  ],
  "transactions": [
    {
      "amount": 50.00,
      "payment_method": "cash"
    }
  ]
}'
```

#### Paiement par Carte
```bash
curl -X POST "http://localhost:8002/sales/" \
-H "Content-Type: application/json" \
-d '{
  "cashier_id": 1,
  "total_amount": 100.00,
  "payment_method": "card",
  "items": [
    {
      "product_id": 2,
      "quantity": 2,
      "unit_price": 50.00
    }
  ],
  "transactions": [
    {
      "amount": 100.00,
      "payment_method": "card",
      "payment_details": {
        "card_number": "**** **** **** 1234",
        "card_type": "visa"
      }
    }
  ]
}'
```

#### Paiement Mobile
```bash
curl -X POST "http://localhost:8002/sales/" \
-H "Content-Type: application/json" \
-d '{
  "cashier_id": 1,
  "total_amount": 75.50,
  "payment_method": "mobile_money",
  "items": [
    {
      "product_id": 3,
      "quantity": 3,
      "unit_price": 25.17
    }
  ],
  "transactions": [
    {
      "amount": 75.50,
      "payment_method": "mobile_money",
      "payment_details": {
        "provider": "orange_money",
        "phone_number": "237123456789"
      }
    }
  ]
}'
```

### 6. Exemples de Mise à Jour de Statut

#### Marquer une Vente comme Terminée
```bash
curl -X PUT "http://localhost:8002/sales/1" \
-H "Content-Type: application/json" \
-d '{
  "status": "completed"
}'
```

#### Annuler une Vente
```bash
curl -X PUT "http://localhost:8002/sales/1" \
-H "Content-Type: application/json" \
-d '{
  "status": "cancelled"
}'
```

#### Marquer une Vente comme Remboursée
```bash
curl -X PUT "http://localhost:8002/sales/1" \
-H "Content-Type: application/json" \
-d '{
  "status": "refunded"
}'
```

## Réponses API

### Exemple de Réponse pour une Vente
```json
{
  "sale": {
    "id": 1,
    "sale_number": "V20240411-00001",
    "cashier_id": 1,
    "customer_id": null,
    "total_amount": 90.0,
    "payment_method": "CASH",
    "status": "PENDING",
    "notes": "Vente sans client",
    "created_at": "2024-04-11T12:00:00",
    "updated_at": "2024-04-11T12:00:00"
  },
  "change_amount": 10.0,
  "items_count": 2,
  "total_amount": 90.0,
  "payment_status": "completed"
}
```

### Exemple de Réponse pour un Client
```json
{
  "id": 1,
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "phone": "+1234567890",
  "address": "123 Main St",
  "created_at": "2024-04-11T12:00:00",
  "updated_at": "2024-04-11T12:00:00"
}
```

### Exemple de Réponse pour une Transaction
```json
{
  "id": 1,
  "sale_id": 1,
  "amount": 90.0,
  "payment_method": "CASH",
  "payment_details": null,
  "amount_received": 100.0,
  "change_amount": 10.0,
  "status": "COMPLETED",
  "created_at": "2024-04-11T12:00:00",
  "updated_at": "2024-04-11T12:00:00"
}
```

## Champs Obligatoires vs Optionnels

### Clients
- Obligatoires : `first_name`, `last_name`
- Optionnels : `email`, `phone`, `address`

### Ventes
- Obligatoires : `cashier_id`, `payment_method`, `items`, `transactions`
- Optionnels : `customer_id`, `notes`

### Transactions
- Obligatoires : `sale_id`, `amount`, `payment_method`
- Optionnels : `payment_details`, `amount_received` (obligatoire pour CASH)

## Erreurs Courantes et Solutions

1. **Erreur 422 Unprocessable Entity**
   - Cause : Données de validation incorrectes
   - Solution : Vérifier que tous les champs obligatoires sont présents et correctement formatés

2. **Erreur 404 Not Found**
   - Cause : Ressource non trouvée
   - Solution : Vérifier que l'ID de la ressource existe

3. **Erreur 400 Bad Request**
   - Cause : Requête mal formulée
   - Solution : Vérifier le format de la requête et les types de données

4. **Erreur 500 Internal Server Error**
   - Cause : Erreur serveur
   - Solution : Vérifier les logs du serveur pour plus de détails

5. **Erreur de Connexion à la Base de Données**
   - Cause : Problème de connexion à MySQL
   - Solution : Vérifier que le service MySQL est en cours d'exécution et que les identifiants sont corrects

## Tests Complets de l'API

Voici une séquence complète de tests pour vérifier toutes les fonctionnalités de l'API.

### 1. Tests des Clients

#### Créer un client
```bash
curl -X POST "http://localhost:8002/customers/" \
-H "Content-Type: application/json" \
-d '{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "phone": "+1234567890",
  "address": "123 Main St"
}'
```

#### Vérifier la création du client
```bash
curl -X GET "http://localhost:8002/customers/1" \
-H "Content-Type: application/json"
```

#### Mettre à jour un client
```bash
curl -X PUT "http://localhost:8002/customers/1" \
-H "Content-Type: application/json" \
-d '{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe.updated@example.com",
  "phone": "+1234567890",
  "address": "456 New St"
}'
```

#### Supprimer un client
```bash
curl -X DELETE "http://localhost:8002/customers/1" \
-H "Content-Type: application/json"
```

### 2. Tests des Ventes

#### Créer une vente simple avec client
```bash
curl -X POST "http://localhost:8002/sales/" \
-H "Content-Type: application/json" \
-d '{
  "cashier_id": 1,
  "customer_id": 1,
  "payment_method": "CASH",
  "items": [
    {
      "product_id": 1,
      "quantity": 2,
      "unit_price": 20.0
    }
  ],
  "transactions": [
    {
      "amount": 40.0,
      "payment_method": "CASH",
      "amount_received": 50.0
    }
  ],
  "notes": "Vente simple avec client"
}'
```

#### Créer une vente sans client
```bash
curl -X POST "http://localhost:8002/sales/" \
-H "Content-Type: application/json" \
-d '{
  "cashier_id": 1,
  "payment_method": "CASH",
  "items": [
    {
      "product_id": 1,
      "quantity": 1,
      "unit_price": 20.0
    }
  ],
  "transactions": [
    {
      "amount": 20.0,
      "payment_method": "CASH",
      "amount_received": 25.0
    }
  ],
  "notes": "Vente sans client"
}'
```

#### Créer une vente avec plusieurs produits
```bash
curl -X POST "http://localhost:8002/sales/" \
-H "Content-Type: application/json" \
-d '{
  "cashier_id": 1,
  "customer_id": 1,
  "payment_method": "CASH",
  "items": [
    {
      "product_id": 1,
      "quantity": 2,
      "unit_price": 20.0
    },
    {
      "product_id": 2,
      "quantity": 1,
      "unit_price": 50.0
    }
  ],
  "transactions": [
    {
      "amount": 90.0,
      "payment_method": "CASH",
      "amount_received": 100.0
    }
  ],
  "notes": "Vente multiple produits"
}'
```

#### Créer une vente avec paiement mixte
```bash
curl -X POST "http://localhost:8002/sales/" \
-H "Content-Type: application/json" \
-d '{
  "cashier_id": 1,
  "customer_id": 1,
  "payment_method": "MIXED",
  "items": [
    {
      "product_id": 1,
      "quantity": 2,
      "unit_price": 50.0
    }
  ],
  "transactions": [
    {
      "amount": 50.0,
      "payment_method": "CARD",
      "payment_details": "1234-5678-9012-3456"
    },
    {
      "amount": 50.0,
      "payment_method": "CASH",
      "amount_received": 60.0
    }
  ],
  "notes": "Paiement mixte : 50€ par carte, 50€ en espèces"
}'
```

### 3. Tests de Lecture et Mise à Jour

#### Liste toutes les ventes
```bash
curl -X GET "http://localhost:8002/sales/" \
-H "Content-Type: application/json"
```

#### Récupérer une vente par ID
```bash
curl -X GET "http://localhost:8002/sales/1" \
-H "Content-Type: application/json"
```

#### Récupérer une vente par numéro
```bash
curl -X GET "http://localhost:8002/sales/number/V20240411-00001" \
-H "Content-Type: application/json"
```

#### Mettre à jour une vente
```bash
curl -X PUT "http://localhost:8002/sales/1" \
-H "Content-Type: application/json" \
-d '{
  "status": "COMPLETED",
  "payment_method": "CARD",
  "notes": "Mise à jour de la vente"
}'
```

### 4. Tests de Suppression

#### Supprimer un client
```bash
curl -X DELETE "http://localhost:8002/customers/1" \
-H "Content-Type: application/json"
```

#### Vérifier la suppression
```bash
curl -X GET "http://localhost:8002/customers/1" \
-H "Content-Type: application/json"
```

## Ordre Recommandé des Tests

Pour tester l'API de manière complète, suivez cet ordre :

1. Création de client
2. Vérification de la création
3. Création de différentes ventes :
   - Vente simple avec client
   - Vente sans client
   - Vente avec plusieurs produits
   - Vente avec paiement mixte
4. Vérification des ventes créées
5. Mise à jour des ventes
6. Mise à jour du client
7. Suppression du client
8. Vérification de la suppression

## Réponses Attendues

### Création Réussie (201)
```json
{
  "id": 1,
  "message": "Ressource créée avec succès"
}
```

### Lecture Réussie (200)
```json
{
  "id": 1,
  "details": "..."
}
```

### Mise à Jour Réussie (200)
```json
{
  "id": 1,
  "message": "Mise à jour réussie"
}
```

### Suppression Réussie (204)
Pas de contenu retourné

### Erreur (404)
```json
{
  "detail": "Ressource non trouvée"
}
``` 