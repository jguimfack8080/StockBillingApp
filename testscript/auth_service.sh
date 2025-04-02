#!/bin/bash

# Configuration
API_BASE_URL="http://localhost:8001"
ADMIN_EMAIL="admin@test.com"
ADMIN_PASSWORD="adminpassword"
USER_FIRST_NAME="Jean"
USER_LAST_NAME="Dupont"
USER_BIRTH_DATE="1995-05-20"
USER_ID_CARD_NUMBER="1234567890"
USER_EMAIL="user1@test.com"
USER_PASSWORD="userpass"
USER_ROLE="manager"

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

# Vérification de la création de l'utilisateur
if echo "$CREATE_USER_RESPONSE" | grep -q "email"; then
    print_success "Utilisateur ${USER_EMAIL} créé avec succès."
else
    print_error "Échec de la création de l'utilisateur : $CREATE_USER_RESPONSE"
    exit 1
fi
