#!/bin/bash

# Configuration
SALES_SERVICE_URL="http://localhost:8002"
AUTH_SERVICE_URL="http://localhost:8001"
TEST_USER_EMAIL="admin@test.com"
TEST_USER_PASSWORD="adminpassword"


# Fonctions utilitaires
log() {
    echo -e "\033[1;34m[INFO]\033[0m $1"
}

error() {
    echo -e "\033[1;31m[ERROR]\033[0m $1"
}

success() {
    echo -e "\033[1;32m[SUCCESS]\033[0m $1"
}

check_response() {
    local response="$1"
    local expected_status="$2"
    
    # Pour le token, vérifier la présence du champ access_token
    if [ "$2" = "token" ]; then
        if [[ "$response" == *"access_token"* ]]; then
            success "Token request successful"
            return 0
        else
            error "Token request failed"
            echo "Response: $response"
            return 1
        fi
    fi
    
    # Pour les réponses de création/lecture, vérifier la présence d'un ID
    if [[ "$response" == *"id"* ]]; then
        success "Request successful"
        return 0
    else
        error "Request failed"
        echo "Response: $response"
        return 1
    fi
}

# Obtenir le token JWT
get_token() {
    log "Getting JWT token..."
    local response=$(curl -s -X POST "$AUTH_SERVICE_URL/auth/token" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "username=$TEST_USER_EMAIL&password=$TEST_USER_PASSWORD")
    
    if check_response "$response" "token"; then
        TOKEN=$(echo "$response" | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
        log "Token obtained successfully"
    else
        error "Failed to get token"
        exit 1
    fi
}

# Tester les endpoints des clients
test_customers() {
    log "Testing customer endpoints..."
    
    # Créer un client
    local create_response=$(curl -s -X POST "$SALES_SERVICE_URL/customers/" \
        -H "Authorization: Bearer $TOKEN" \
        -H "Content-Type: application/json" \
        -d '{
            "first_name": "Test",
            "last_name": "Customer",
            "email": "customer@example.com",
            "phone": "1234567890",
            "address": "123 Test Street"
        }')
    
    if check_response "$create_response" "200"; then
        local customer_id=$(echo "$create_response" | grep -o '"id":[0-9]*' | cut -d':' -f2)
        log "Customer created with ID: $customer_id"
        
        # Tester la création d'une vente avec ce client
        test_sales "$customer_id"
    else
        error "Failed to create customer"
    fi
}

# Tester les endpoints des ventes
test_sales() {
    local customer_id="$1"
    log "Testing sales endpoints with customer ID: $customer_id..."
    
    # Créer une vente
    local create_response=$(curl -s -X POST "$SALES_SERVICE_URL/sales/" \
        -H "Authorization: Bearer $TOKEN" \
        -H "Content-Type: application/json" \
        -d '{
            "cashier_id": 1,
            "customer_id": '$customer_id',
            "payment_method": "CASH",
            "notes": "Test sale",
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
                    "payment_method": "CASH",
                    "payment_details": "Cash payment",
                    "amount_received": 30.00
                }
            ]
        }')
    
    if check_response "$create_response" "200"; then
        local sale_id=$(echo "$create_response" | grep -o '"sale":{"id":[0-9]*' | cut -d':' -f3)
        log "Sale created with ID: $sale_id"
        
        # Récupérer toutes les ventes
        local get_all_response=$(curl -s -X GET "$SALES_SERVICE_URL/sales/" \
            -H "Authorization: Bearer $TOKEN")
        
        if check_response "$get_all_response" "200"; then
            log "Successfully retrieved all sales"
        else
            error "Failed to retrieve all sales"
        fi
        
        # Récupérer une vente spécifique
        local get_one_response=$(curl -s -X GET "$SALES_SERVICE_URL/sales/$sale_id" \
            -H "Authorization: Bearer $TOKEN")
        
        if check_response "$get_one_response" "200"; then
            log "Successfully retrieved sale with ID: $sale_id"
        else
            error "Failed to retrieve sale with ID: $sale_id"
        fi
        
        # Mettre à jour une vente
        local update_response=$(curl -s -X PUT "$SALES_SERVICE_URL/sales/$sale_id" \
            -H "Authorization: Bearer $TOKEN" \
            -H "Content-Type: application/json" \
            -d '{
                "status": "COMPLETED",
                "payment_method": "CASH",
                "notes": "Updated sale"
            }')
        
        if check_response "$update_response" "200"; then
            log "Successfully updated sale with ID: $sale_id"
        else
            error "Failed to update sale with ID: $sale_id"
        fi
        
        # Tester les transactions avec cette vente
        test_transactions "$sale_id"
    else
        error "Failed to create sale"
    fi
}

# Tester les endpoints des transactions
test_transactions() {
    local sale_id="$1"
    log "Testing transaction endpoints with sale ID: $sale_id..."
    
    # Créer une transaction
    local create_response=$(curl -s -X POST "$SALES_SERVICE_URL/transactions/" \
        -H "Authorization: Bearer $TOKEN" \
        -H "Content-Type: application/json" \
        -d '{
            "sale_id": '$sale_id',
            "amount": 21.98,
            "payment_method": "CASH",
            "payment_details": "Cash payment",
            "amount_received": 30.00
        }')
    
    if check_response "$create_response" "200"; then
        local transaction_id=$(echo "$create_response" | grep -o '"id":[0-9]*' | cut -d':' -f2)
        log "Transaction created with ID: $transaction_id"
        
        # Mettre à jour le statut de la transaction
        local update_response=$(curl -s -X PUT "$SALES_SERVICE_URL/transactions/$transaction_id/status" \
            -H "Authorization: Bearer $TOKEN" \
            -H "Content-Type: application/json" \
            -d '{
                "status": "COMPLETED"
            }')
        
        if check_response "$update_response" "200"; then
            log "Successfully updated transaction status"
        else
            error "Failed to update transaction status"
        fi
    else
        error "Failed to create transaction"
    fi
}

# Exécuter les tests
get_token
test_customers 