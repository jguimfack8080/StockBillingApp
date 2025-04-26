# Stock Service

Service de gestion de stock pour l'application StockBilling. Ce service gère les produits, les catégories et les mouvements de stock.

## Fonctionnalités

- Gestion des catégories (CRUD)
- Gestion des produits (CRUD)
  - Support des numéros d'article (optionnel)
  - Association avec des catégories
- Gestion des mouvements de stock
  - Entrées de stock
  - Sorties de stock
  - Suivi des quantités

## Prérequis

- Python 3.8+
- MySQL
- Docker (optionnel)

## Installation

1. Cloner le repository
2. Créer un environnement virtuel :
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
.\venv\Scripts\activate  # Windows
```

3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

4. Configurer les variables d'environnement :
```bash
cp .env.example .env
# Éditer .env avec vos configurations
```

## Configuration

Le fichier `.env` doit contenir :

```env
DATABASE_URL=mysql+pymysql://stock_user:stock_password@stockbilling_mysql_stock:3306/stock_db
SECRET_KEY=votre_secret_key
ALGORITHM=HS256
AUTH_SERVICE_URL=http://auth_service:8000
```

## Démarrage

### Avec Docker

```bash
docker-compose up
```

### Manuellement

1. Démarrer le service :
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8003
```

## API Endpoints

### Catégories

- `POST /categories/` - Créer une catégorie
- `GET /categories/` - Lister toutes les catégories
- `GET /categories/{id}` - Obtenir une catégorie
- `PUT /categories/{id}` - Mettre à jour une catégorie
- `DELETE /categories/{id}` - Supprimer une catégorie

### Produits

- `POST /products/` - Créer un produit
- `GET /products/` - Lister tous les produits
- `GET /products/{id}` - Obtenir un produit par ID
- `GET /products/article/{article_number}` - Obtenir un produit par numéro d'article
- `PUT /products/{id}` - Mettre à jour un produit
- `DELETE /products/{id}` - Supprimer un produit

### Mouvements de Stock

- `POST /stock-movements/` - Créer un mouvement de stock
- `GET /stock-movements/` - Lister tous les mouvements
- `GET /stock-movements/product/{product_id}` - Obtenir les mouvements d'un produit
- `GET /stock-movements/product/article/{article_number}` - Obtenir les mouvements par numéro d'article

## Tests

Pour tester l'API, utilisez les commandes curl fournies dans `test_commands.txt`.

## Sécurité

- Authentification requise pour toutes les routes
- Rôles utilisateur :
  - `admin` : Accès complet
  - `user` : Lecture seule

## Base de données

Le schéma de la base de données est défini dans `init.sql`. Les tables principales sont :

- `categories`
- `products`
- `product_categories`
- `stock_movements`

## Contribution

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request 