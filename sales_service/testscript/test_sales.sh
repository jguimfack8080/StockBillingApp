#!/bin/bash

# Configuration
SALES_SERVICE_URL="http://localhost:8002"
AUTH_SERVICE_URL="http://localhost:8001"
TEST_USER_EMAIL="admin@test.com"
TEST_USER_PASSWORD="adminpassword"

# Couleurs pour l'affichage
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[1;34m'
NC='\033[0m' # No Color

# Variables pour stocker les IDs
SALE_ID=""
SALE_NUMBER=""
AUTH_TOKEN=""

# Fonctions utilitaires
log() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

# Vérifier la réponse et extraire les données
check_response() {
    local response="$1"
    local expected_type="$2"

    echo "Response received: $response"

    case "$expected_type" in
        "token")
            [[ "$response" == *"access_token"* ]] && success "Token request successful" && return 0 || error "Token request failed" && return 1
            ;;
        "sale")
            [[ "$response" == *"\"sale\""* || "$response" == *"\"id\""* ]] && success "Sale operation successful" && return 0 || error "Sale operation failed" && return 1
            ;;
        * )
            [[ "$response" == *"\"id\""* ]] && success "Operation successful" && return 0 || error "Operation failed" && return 1
            ;;
    esac
}

# Vérifier la disponibilité de l'API
check_api_availability() {
    echo -e "${YELLOW}Checking API availability...${NC}"
    if curl -s "$SALES_SERVICE_URL/" > /dev/null; then
        echo -e "${GREEN}API is available${NC}\n"
    else
        echo -e "${RED}API is not available. Please make sure the service is running.${NC}\n"
        exit 1
    fi
}

# Obtenir un token JWT
get_token() {
    log "Getting JWT token..."
    local response=$(curl -s -X POST "$AUTH_SERVICE_URL/auth/token" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "username=$TEST_USER_EMAIL&password=$TEST_USER_PASSWORD")

    if check_response "$response" "token"; then
        AUTH_TOKEN=$(echo "$response" | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
        log "Token obtained: $AUTH_TOKEN"
    else
        error "Failed to get token"
        exit 1
    fi
}

# Extraire l'ID d'une réponse JSON
extract_id() {
    local json="$1"
    echo "$json" | grep -o '"id":[0-9]*' | cut -d':' -f2
}

# Extraire un numéro de vente
extract_sale_number() {
    local json="$1"
    echo "$json" | grep -o '"sale_number":"[^"]*"' | cut -d'"' -f4
}

# Afficher une réponse
print_response() {
    local endpoint="$1"
    local response="$2"
    local status_code=$(echo "$response" | tail -n1)
    local body=$(echo "$response" | sed '$d')

    echo -e "\n${YELLOW}=== $endpoint ===${NC}"
    echo -e "Status Code: $status_code"
    echo -e "Response Body:"
    echo "$body" | jq '.'
    echo "----------------------------------------"
}

# Résumé rapide
test_endpoint_echo() {
    local test_name="$1"
    local result="$2"
    echo -e "${YELLOW}Testing: $test_name${NC}"
    echo "$result"
}

### DÉBUT DES TESTS ###

check_api_availability
get_token

# === SALES ===
log "Testing sales endpoints..."

# Créer une vente
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$SALES_SERVICE_URL/sales/" \
    -H "Authorization: Bearer $AUTH_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
        "cashier_id": 1,
        "customer_id": 1,
        "payment_method": "CASH",
        "items": [
            {
                "product_id": 1,
                "quantity": 2,
                "unit_price": 10.50
            }
        ],
        "transactions": [
            {
                "amount": 21.00,
                "payment_method": "CASH",
                "amount_received": 25.00,
                "payment_details": "Test transaction"
            }
        ],
        "notes": "Test sale"
    }')

print_response "POST /sales/" "$RESPONSE"
BODY=$(echo "$RESPONSE" | sed '$d')
SALE_ID=$(extract_id "$BODY")
SALE_NUMBER=$(extract_sale_number "$BODY")
test_endpoint_echo "Sale creation" "Sale ID: $SALE_ID, Sale Number: $SALE_NUMBER"

# Créer des ventes en masse
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$SALES_SERVICE_URL/sales/bulk" \
    -H "Authorization: Bearer $AUTH_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
        "cashier_id": 1,
        "customer_id": 1,
        "sales": [
            {
                "payment_method": "CASH",
                "items": [
                    {
                        "product_id": 1,
                        "quantity": 1,
                        "unit_price": 10.50
                    }
                ],
                "transactions": [
                    {
                        "amount": 10.50,
                        "payment_method": "CASH",
                        "amount_received": 15.00,
                        "payment_details": "Test transaction 1"
                    }
                ]
            },
            {
                "payment_method": "CASH",
                "items": [
                    {
                        "product_id": 2,
                        "quantity": 2,
                        "unit_price": 5.25
                    }
                ],
                "transactions": [
                    {
                        "amount": 10.50,
                        "payment_method": "CASH",
                        "amount_received": 20.00,
                        "payment_details": "Test transaction 2"
                    }
                ]
            }
        ]
    }')

print_response "POST /sales/bulk" "$RESPONSE"
test_endpoint_echo "Bulk sales creation" "Done"

# Liste des ventes
RESPONSE=$(curl -s -w "\n%{http_code}" -H "Authorization: Bearer $AUTH_TOKEN" "$SALES_SERVICE_URL/sales/")
print_response "GET /sales/" "$RESPONSE"

# Vente par ID
RESPONSE=$(curl -s -w "\n%{http_code}" -H "Authorization: Bearer $AUTH_TOKEN" "$SALES_SERVICE_URL/sales/$SALE_ID")
print_response "GET /sales/$SALE_ID" "$RESPONSE"

# Vente par numéro
RESPONSE=$(curl -s -w "\n%{http_code}" -H "Authorization: Bearer $AUTH_TOKEN" "$SALES_SERVICE_URL/sales/number/$SALE_NUMBER")
print_response "GET /sales/number/$SALE_NUMBER" "$RESPONSE"

# Mise à jour de la vente
RESPONSE=$(curl -s -w "\n%{http_code}" -X PUT "$SALES_SERVICE_URL/sales/$SALE_ID" \
    -H "Authorization: Bearer $AUTH_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"status": "COMPLETED", "notes": "Updated test sale"}')
print_response "PUT /sales/$SALE_ID" "$RESPONSE"

# Suppression de la vente
RESPONSE=$(curl -s -w "\n%{http_code}" -X DELETE "$SALES_SERVICE_URL/sales/$SALE_ID" \
    -H "Authorization: Bearer $AUTH_TOKEN")
print_response "DELETE /sales/$SALE_ID" "$RESPONSE"

success "All sales endpoint tests completed successfully!" 