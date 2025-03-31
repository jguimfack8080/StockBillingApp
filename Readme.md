## StockBillingApp - Logiciel de Facturation et Gestion de Stocks Automatisé

## Description du Projet

**StockBillingApp** est une application de gestion des stocks et de facturation entièrement automatisée, développée en Python avec une interface graphique conviviale, conçue pour être utilisée sur des postes de travail sous Windows. Cette application offre une solution complète pour automatiser la gestion des ventes, des stocks, des paiements, des clients et des fournisseurs. Elle permet d’effectuer toutes les tâches de manière rapide et sans intervention manuelle, avec des calculs automatiques, des alertes de réapprovisionnement, et la génération automatique de rapports de ventes et de bénéfices.

### Objectifs Principaux du Projet

- **Automatisation complète** : Éviter toute interaction manuelle, y compris les calculs de taxes, la mise à jour des stocks, les rapports, et l'envoi d'alertes de réapprovisionnement.
- **Interface conviviale** : Offrir une expérience fluide et rapide pour les caissiers, les managers, et les administrateurs.
- **Suivi des performances** : Permettre aux managers et administrateurs de suivre facilement les ventes, les bénéfices, et l'état des stocks.
- **Gestion des paiements** : Prise en charge des paiements en espèces, par carte bancaire, et par Mobile Money.
- **Architecture modulaire** : Utilisation de microservices pour une gestion indépendante des fonctionnalités (ventes, stocks, paiements, etc.).

---

## Fonctionnalités Principales

### 1️⃣ **Ventes et Facturation Automatisées**

- **Interface de caisse simple et rapide** : L'interface est conçue pour permettre aux caissiers d'enregistrer les ventes rapidement et efficacement, réduisant les erreurs et les délais de traitement.
- **Ajout de produits via scanner de code-barres ou manuel** : Les caissiers peuvent scanner les produits avec un lecteur de code-barres ou saisir les informations manuellement. Le système est capable de gérer un grand nombre de produits sans nécessiter d'entrée manuelle répétitive.
- **Calcul automatique du total avec taxes** : Le total de chaque vente, incluant les taxes applicables, est calculé automatiquement à partir des paramètres définis par l'administrateur.
- **Impression de tickets et factures PDF** : Après chaque vente, le système génère automatiquement un ticket imprimé pour le client et une facture au format PDF pour l'archivage.
- **Reçus numériques** : Envoi automatique de reçus par SMS ou email après chaque transaction, garantissant une traçabilité et un suivi client optimisés.

### 2️⃣ **Gestion des Stocks Automatisée**

- **Suivi des entrées et sorties de produits** : Le stock est automatiquement mis à jour lors des ventes ou des réapprovisionnements. La base de données est en temps réel, ce qui permet une gestion précise des quantités disponibles.
- **Alertes de réapprovisionnement automatiques** : Lorsqu’un produit atteint son seuil de stock minimal, une alerte par email est envoyée à l’administrateur pour lui rappeler de réapprovisionner le stock.
- **Mise à jour automatique du stock** : L'administrateur peut ajouter des quantités de produits manuellement, et le stock est immédiatement mis à jour dans la base de données.
- **Suivi des fournisseurs automatisé** : Le système garde trace des fournisseurs pour chaque produit et peut générer automatiquement des commandes pour réapprovisionner les stocks en cas de besoin.
- **Gestion des lots et dates de péremption** : Alerte en cas de produits proches de leur date d’expiration.

### 3️⃣ **Modes de Paiement Automatisés**

- **Espèces (Cash)** : Le caissier entre simplement le montant payé par le client. Le système calcule automatiquement le montant à rendre et met à jour les transactions.
- **Carte bancaire (via TPE)** : Le paiement par carte est intégré via un terminal de paiement électronique (TPE). Dès que le paiement est validé, le système enregistre la transaction sans besoin d’intervention manuelle.
- **Mobile Money** : Le paiement par Mobile Money est intégré et fonctionne de manière automatique pour enregistrer les paiements sans intervention manuelle.
- **Gestion de la trésorerie** : Suivi des encaissements et des fonds disponibles.

### 4️⃣ **Gestion des Clients & Fournisseurs**

- **Fichier Clients et Historique des Achats** : Le système garde une trace complète des achats des clients, ce qui permet de suivre les habitudes d'achat et de proposer des offres personnalisées.
- **Suivi des dettes et paiements** : Le système enregistre tous les paiements des clients et génère des rappels automatiques en cas de retard de paiement.
- **Commandes et livraisons automatisées** : Lorsque les clients passent des commandes, celles-ci sont enregistrées automatiquement et envoyées aux fournisseurs. Le suivi des livraisons se fait également de manière automatique.
- **Programme de fidélité** : Points de fidélité pour les clients réguliers, échangeables contre des réductions.

### 5️⃣ **Rapports et Statistiques Automatisées**

- **Rapports de ventes par jour/mois/produit** : Des rapports détaillés des ventes sont générés automatiquement à intervalles réguliers. Ces rapports peuvent être consultés par les administrateurs et managers pour analyser les performances.
- **Rapports des produits les plus vendus** : Le système génère des rapports automatiques des produits les plus populaires, offrant des informations précieuses pour la gestion des stocks.
- **Suivi des bénéfices automatisé** : Le calcul des marges bénéficiaires est effectué automatiquement et peut être consulté via des rapports sur les bénéfices réalisés par produit ou par période.
- **Comparaison de périodes** : Analyser les performances vs. la même période l’année dernière.

### 6️⃣ **Sécurité et Accès Multi-Utilisateurs Automatisés**

- **Gestion des rôles d'utilisateur automatique** : L’administrateur peut définir les rôles des utilisateurs (caissiers, managers, administrateurs) et attribuer des privilèges spécifiques. Le système applique ces privilèges automatiquement lors de la connexion de l’utilisateur.
- **Protection par mot de passe et cryptage** : Tous les mots de passe sont cryptés à l’aide d'algorithmes de sécurité robustes pour garantir la protection des informations sensibles.
- **Audit des actions** : Toutes les actions des utilisateurs (ventes, paiements, réapprovisionnements) sont automatiquement enregistrées dans un journal des événements pour assurer une traçabilité complète.
- **Verrouillage automatique** : Session bloquée après 5 minutes d’inactivité.

---

## Rôles Utilisateurs et Fonctionnalités

### **Caissier**

- **Interface de caisse simple et rapide** : L'interface permet d'ajouter rapidement des produits à une vente en scannant des codes-barres ou en les saisissant manuellement.
- **Calcul automatique du total avec taxes** : Le système calcule automatiquement le montant total, taxes incluses, sans que le caissier ait à entrer ces informations manuellement.
- **Impression des tickets et factures** : Après chaque vente, un ticket est imprimé pour le client, et une facture PDF est générée automatiquement pour l’archivage.
- **Saisie de quantité optimisée** : Lorsqu'un produit est scanné, si le client en achète plusieurs exemplaires, le caissier peut scanner le produit une seule fois et entrer directement le nombre d'unités, simplifiant ainsi le processus de facturation.
- **Suppression d'un produit non payé** : Si le client décide de ne pas acheter un produit et que la transaction n'a pas encore été validée, le caissier peut supprimer ce produit de la liste de la vente, garantissant ainsi une facturation précise et évitant tout malentendu lors de la validation du paiement.
- **Gestion des retours et échanges** : Si un client revient avec un produit déjà acheté, le caissier peut initier le processus de retour. Après contrôle du produit, la facture correspondante doit être scannée pour valider le retour. Le système met alors à jour le stock et enregistre le retour, facilitant ainsi les remboursements ou échanges tout en assurant une traçabilité complète.

### **Admin**

- **Paramétrage des taxes et des produits** : L'administrateur peut configurer les taux de taxes applicables et ajouter, modifier ou supprimer des produits du système.
- **Gestion des utilisateurs** : L'administrateur peut créer de nouveaux comptes pour un nouveau admin, les caissiers et managers, leur attribuer des rôles et les privilèges appropriés.
- **Gestion des stocks et des fournisseurs** : L’administrateur peut gérer les stocks, définir des seuils minimaux pour les produits, et enregistrer les informations sur les fournisseurs.
- **Visualisation des rapports de vente** : L'administrateur peut consulter des rapports détaillés sur les ventes, les produits les plus vendus, les bénéfices générés, et les performances globales du système.

### **Manager**

- **Suivi des ventes** : Le manager peut consulter les ventes effectuées par chaque caissier, obtenir des rapports détaillés des ventes quotidiennes ou mensuelles, et identifier les produits les plus populaires.
- **Suivi des bénéfices** : Le manager peut analyser les bénéfices générés, identifier les produits les plus rentables et ajuster la stratégie de vente en conséquence.
- **Suivi des performances des caissiers** : Le manager peut consulter les performances de chaque caissier, notamment en termes de ventes réalisées et de transactions traitées.

---

## Architecture Microservices

### **Modules Indépendants**
1. **Service de Ventes** :
   - Gère les transactions, les factures, et les retours.
   - Expose une API REST pour l’interface utilisateur.

2. **Service de Stocks** :
   - Suivi des entrées/sorties, alertes de réapprovisionnement.
   - API pour la gestion des produits et des fournisseurs.

3. **Service de Paiements** :
   - Gère les modes de paiement et la trésorerie.
   - API pour l’intégration avec les TPE et Mobile Money.

4. **Service de Rapports** :
   - Génère des rapports de ventes, stocks, et bénéfices.
   - API pour exporter des données en CSV/PDF.

5. **Service d’Authentification** :
   - Gère les utilisateurs, les rôles, et les permissions.
   - API pour la connexion et la gestion des sessions.

### **Communication entre Microservices**
- **Protocole HTTP/JSON** : Les services communiquent via des API REST.
- **Message Broker (Optionnel)** : Utilisation de RabbitMQ ou ZeroMQ pour une communication asynchrone (ex: notifications d’alertes de stock).

---

## Technologies Utilisées

- **Python 3.10+** : Langage principal pour les microservices.
- **FastAPI** : Framework pour créer des API RESTful performantes.
- **MySQL** : Base de données locale pour chaque service.
- **PyQt5** : Interface utilisateur pour la partie desktop.
- **Docker** : Conteneurisation des microservices pour un déploiement facile.
- **Cryptography** : Chiffrement des données sensibles (mots de passe, transactions).

---

## Installation

1. **Cloner le repository** :
   ```bash
   git clone https://github.com/jguimfack8080/StockBillingApp.git
   cd StockBillingApp
   ```

2. **Démarrer les Microservices** :
   ```bash
   docker-compose up --build
   ```

3. **Accéder à l'Application** :
   - Interface utilisateur : `http://localhost:8000`
   - API Documentation (Swagger) : `http://localhost:8000/docs`

---

## Conclusion

**StockBillingApp** est une solution complète pour la gestion des stocks et la facturation, qui permet d'automatiser toutes les étapes du processus, des ventes à la gestion des stocks, en passant par les paiements et les rapports. Ce logiciel permet aux entreprises d'optimiser leur fonctionnement en réduisant les tâches manuelles et en augmentant l'efficacité opérationnelle.

---

## Auteurs

- **Jordan Guimfack Jeuna**  
Développeur principal

---

## Licence

Ce projet est sous **licence MIT**.

