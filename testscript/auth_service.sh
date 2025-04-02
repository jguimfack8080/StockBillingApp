#!/bin/bash

# Configuration
API_BASE_URL="http://localhost:8001"
ADMIN_EMAIL="admin@test.com"
ADMIN_PASSWORD="adminpassword"
USER_FIRST_NAME="Jean"
USER_LAST_NAME="Dupont"
USER_BIRTH_DATE="1995-05-20"
USER_ID_CARD_NUMBER="12345678902"
USER_EMAIL="user2@test.com"
USER_PASSWORD="userpass"
USER_ROLE="cashier"
NEW_USER_EMAIL="user1_updated@test.com"
NEW_USER_ROLE="cashier"  # New role for updating
DEACTIVATION_REASON="Inactive for too long"

# Fonction pour afficher les résultats en couleur
function print_success() {
    echo -e "\e[32m[SUCCESS]\e[0m $1"
}

function print_error() {
    echo -e "\e[31m[ERROR]\e[0m $1"
}

# Vérifier si le serveur tourne
echo "1️⃣ Vérification du serveur..."
if curl -s "${API_BASE_URL}" | grep -q "OK"; then
    print_success "Le serveur est en ligne."
else
    print_error "Le serveur ne répond pas. Lance-le avec 'uvicorn main:app --reload'"
    exit 1
fi

# Obtenir un token pour l'admin
echo "2️⃣ Récupération du token d'admin..."
ADMIN_TOKEN=$(curl -s -X POST "${API_BASE_URL}/auth/token" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=${ADMIN_EMAIL}&password=${ADMIN_PASSWORD}" | jq -r '.access_token')

if [[ -z "$ADMIN_TOKEN" || "$ADMIN_TOKEN" == "null" ]]; then
    print_error "Impossible d'obtenir le token d'admin."
    exit 1
else
    print_success "Token d'admin récupéré."
fi

# Créer un utilisateur (caissier)
echo "3️⃣ Création d'un utilisateur (${USER_EMAIL})..."
CREATE_USER_RESPONSE=$(curl -s -X POST "${API_BASE_URL}/users/" \
    -H "Authorization: Bearer ${ADMIN_TOKEN}" \
    -H "Content-Type: application/json" \
    -d "{
        \"first_name\": \"${USER_FIRST_NAME}\",
        \"last_name\": \"${USER_LAST_NAME}\",
        \"birth_date\": \"${USER_BIRTH_DATE}\",
        \"id_card_number\": \"${USER_ID_CARD_NUMBER}\",
        \"email\": \"${USER_EMAIL}\",
        \"password\": \"${USER_PASSWORD}\",
        \"role\": \"${USER_ROLE}\"
    }")

# Afficher la réponse du serveur lors de la création de l'utilisateur
echo "Réponse de la création de l'utilisateur : $CREATE_USER_RESPONSE"

# Vérification de la création de l'utilisateur
if echo "$CREATE_USER_RESPONSE" | grep -q "email"; then
    print_success "Utilisateur ${USER_EMAIL} créé avec succès."
else
    print_error "Échec de la création de l'utilisateur : $CREATE_USER_RESPONSE"
    exit 1
fi

# Mettre à jour l'utilisateur
USER_ID=$(echo "$CREATE_USER_RESPONSE" | jq -r '.id')  # Récupérer l'ID de l'utilisateur créé
echo "4️⃣ Mise à jour de l'utilisateur (${USER_ID})..."

UPDATE_USER_RESPONSE=$(curl -s -X PUT "${API_BASE_URL}/users/${USER_ID}" \
    -H "Authorization: Bearer ${ADMIN_TOKEN}" \
    -H "Content-Type: application/json" \
    -d "{
        \"email\": \"${NEW_USER_EMAIL}\",
        \"role\": \"${NEW_USER_ROLE}\"
    }")

# Afficher la réponse du serveur lors de la mise à jour de l'utilisateur
echo "Réponse de la mise à jour de l'utilisateur : $UPDATE_USER_RESPONSE"

# Vérification de la mise à jour de l'utilisateur
if echo "$UPDATE_USER_RESPONSE" | grep -q "email"; then
    print_success "Utilisateur ${USER_ID} mis à jour avec succès."
else
    print_error "Échec de la mise à jour de l'utilisateur : $UPDATE_USER_RESPONSE"
    exit 1
fi

# Tester la récupération de tous les utilisateurs
echo "5️⃣ Récupération de tous les utilisateurs..."
GET_USERS_RESPONSE=$(curl -s -X GET "${API_BASE_URL}/users/" \
    -H "Authorization: Bearer ${ADMIN_TOKEN}" \
    -H "Accept: application/json")

# Afficher la réponse du serveur lors de la récupération des utilisateurs
echo "$GET_USERS_RESPONSE"

# Désactivation de l'utilisateur
echo "6️⃣ Désactivation de l'utilisateur (${USER_ID}) avec raison : '${DEACTIVATION_REASON}'..."
DEACTIVATE_USER_RESPONSE=$(curl -s -X PUT "${API_BASE_URL}/users/deactivate/${USER_ID}" \
    -H "Authorization: Bearer ${ADMIN_TOKEN}" \
    -H "Content-Type: application/json" \
    -d "{
        \"reason\": \"${DEACTIVATION_REASON}\"
    }")

# Afficher la réponse du serveur lors de la désactivation
echo "Réponse de la désactivation de l'utilisateur : $DEACTIVATE_USER_RESPONSE"

# Vérification de la désactivation de l'utilisateur
if echo "$DEACTIVATE_USER_RESPONSE" | grep -q "message"; then
    print_success "Utilisateur ${USER_ID} désactivé avec succès pour la raison '${DEACTIVATION_REASON}'."
else
    print_error "Échec de la désactivation de l'utilisateur : $DEACTIVATE_USER_RESPONSE"
    exit 1
fi
