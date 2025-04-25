#!/bin/bash

BASE_URL="http://localhost:8002/sales"
HEADER="Content-Type: application/json"

# Création d'une vente
echo "⏳ Création d'une vente (draft)..."
CREATE_RESPONSE=$(curl -s -X POST $BASE_URL/ \
-H "$HEADER" \
-d '{
  "cashier_id": 1,
  "notes": "Commande test",
  "items": [
    {"product_id": 101, "quantity": 2, "unit_price": 5.0},
    {"product_id": 102, "quantity": 1, "unit_price": 10.0}
  ]
}')
SALE_ID=$(echo "$CREATE_RESPONSE" | jq -r '.sale.id')
SALE_NUMBER=$(echo "$CREATE_RESPONSE" | jq -r '.sale.sale_number')
echo "✅ Vente créée avec ID: $SALE_ID et Numéro: $SALE_NUMBER"

# Paiement CASH uniquement
echo "📤 Paiement CASH uniquement..."
PAYMENT_CASH=$(curl -s -X POST $BASE_URL/$SALE_ID/pay \
-H "$HEADER" \
-d '{
  "transactions": [
    {
      "amount": 20.0,
      "payment_method": "CASH",
      "amount_received": 20.0
    }
  ]
}')
echo "$PAYMENT_CASH" | jq

# Paiement MIXTE (CASH + TRANSFER)
echo "📤 Paiement MIXTE (CASH + TRANSFER)..."
SALE_ID2=$(curl -s -X POST $BASE_URL/ \
-H "$HEADER" \
-d '{
  "cashier_id": 1,
  "notes": "Vente mixte CASH+TRANSFER",
  "items": [
    {"product_id": 103, "quantity": 2, "unit_price": 10.0}
  ]
}' | jq -r '.sale.id')

PAYMENT_MIXTE_CASH_TRANSFER=$(curl -s -X POST $BASE_URL/$SALE_ID2/pay \
-H "$HEADER" \
-d '{
  "transactions": [
    {
      "amount": 10.0,
      "payment_method": "CASH",
      "amount_received": 10.0
    },
    {
      "amount": 10.0,
      "payment_method": "TRANSFER",
      "payment_details": {
        "operator": "Orange",
        "phone_number": "+237612345678"
      }
    }
  ]
}')
echo "$PAYMENT_MIXTE_CASH_TRANSFER" | jq

# Paiement MIXTE (CASH + CARD)
echo "📤 Paiement MIXTE (CASH + CARD)..."
SALE_ID3=$(curl -s -X POST $BASE_URL/ \
-H "$HEADER" \
-d '{
  "cashier_id": 1,
  "notes": "Vente mixte CASH+CARD",
  "items": [
    {"product_id": 104, "quantity": 1, "unit_price": 25.0}
  ]
}' | jq -r '.sale.id')

PAYMENT_MIXTE_CASH_CARD=$(curl -s -X POST $BASE_URL/$SALE_ID3/pay \
-H "$HEADER" \
-d '{
  "transactions": [
    {
      "amount": 10.0,
      "payment_method": "CASH",
      "amount_received": 10.0
    },
    {
      "amount": 15.0,
      "payment_method": "CARD"
    }
  ]
}')
echo "$PAYMENT_MIXTE_CASH_CARD" | jq

# Paiement MIXTE (TRANSFER + CARD)
echo "📤 Paiement MIXTE (TRANSFER + CARD)..."
SALE_ID4=$(curl -s -X POST $BASE_URL/ \
-H "$HEADER" \
-d '{
  "cashier_id": 1,
  "notes": "Vente mixte TRANSFER+CARD",
  "items": [
    {"product_id": 105, "quantity": 2, "unit_price": 15.0}
  ]
}' | jq -r '.sale.id')

PAYMENT_MIXTE_TRANSFER_CARD=$(curl -s -X POST $BASE_URL/$SALE_ID4/pay \
-H "$HEADER" \
-d '{
  "transactions": [
    {
      "amount": 10.0,
      "payment_method": "TRANSFER",
      "payment_details": {
        "operator": "MTN",
        "phone_number": "+237699998888"
      }
    },
    {
      "amount": 20.0,
      "payment_method": "CARD"
    }
  ]
}')
echo "$PAYMENT_MIXTE_TRANSFER_CARD" | jq

# Annulation d'une vente
echo "🚫 Annulation d'une vente..."
CANCEL_RESPONSE=$(curl -s -X PUT $BASE_URL/$SALE_ID \
-H "$HEADER" \
-d '{
  "status": "CANCELLED",
  "notes": "Client a annulé la commande"
}')
echo "$CANCEL_RESPONSE" | jq

# Récupération de toutes les ventes
echo "📋 Récupération de toutes les ventes..."
ALL_SALES=$(curl -s $BASE_URL/)
echo "$ALL_SALES" | jq

# Récupération de la vente par ID
echo "🔍 Récupération de la vente par ID ($SALE_ID)..."
SALE_BY_ID=$(curl -s $BASE_URL/$SALE_ID)
echo "$SALE_BY_ID" | jq

# Récupération de la vente par numéro
echo "🔍 Récupération de la vente par numéro ($SALE_NUMBER)..."
SALE_BY_NUMBER=$(curl -s $BASE_URL/number/$SALE_NUMBER)
echo "$SALE_BY_NUMBER" | jq

# Vente avec paiement 100% CASH
echo "----------------------------------------"
echo "🛒 Vente avec paiement 100% CASH"
RESPONSE_CASH=$(curl -s -X POST $BASE_URL/ \
-H "$HEADER" \
-d '{
  "cashier_id": 1,
  "notes": "Vente CASH",
  "items": [{"product_id": 201, "quantity": 2, "unit_price": 5.0}]
}')
SALE_ID_CASH=$(echo $RESPONSE_CASH | jq -r '.sale.id')
pay_sale $SALE_ID_CASH '[{"amount": 10.0, "payment_method": "CASH", "amount_received": 10.0}]'

# Vente avec paiement 100% TRANSFER
echo "----------------------------------------"
echo "🛒 Vente avec paiement 100% TRANSFER"
RESPONSE_TRANSFER=$(curl -s -X POST $BASE_URL/ \
-H "$HEADER" \
-d '{
  "cashier_id": 1,
  "notes": "Vente TRANSFER",
  "items": [{"product_id": 202, "quantity": 1, "unit_price": 15.0}]
}')
SALE_ID_TRANSFER=$(echo $RESPONSE_TRANSFER | jq -r '.sale.id')
pay_sale $SALE_ID_TRANSFER '[{
  "amount": 15.0,
  "payment_method": "TRANSFER",
  "payment_details": {
    "operator": "MTN",
    "phone_number": "+237612345678"
  }
}]'

# Vente avec paiement 100% CARD
echo "----------------------------------------"
echo "🛒 Vente avec paiement 100% CARD"
RESPONSE_CARD=$(curl -s -X POST $BASE_URL/ \
-H "$HEADER" \
-d '{
  "cashier_id": 1,
  "notes": "Vente CARD",
  "items": [{"product_id": 203, "quantity": 1, "unit_price": 20.0}]
}')
SALE_ID_CARD=$(echo $RESPONSE_CARD | jq -r '.sale.id')
pay_sale $SALE_ID_CARD '[{"amount": 20.0, "payment_method": "CARD"}]'

# Vente avec paiement MIXTE CASH + TRANSFER
echo "----------------------------------------"
echo "🛒 Vente avec paiement MIXTE CASH + TRANSFER"
RESPONSE_MIXTE_CASH_TRANSFER=$(curl -s -X POST $BASE_URL/ \
-H "$HEADER" \
-d '{
  "cashier_id": 1,
  "notes": "Vente CASH+TRANSFER",
  "items": [{"product_id": 204, "quantity": 3, "unit_price": 10.0}]
}')
SALE_ID_MIXTE_CASH_TRANSFER=$(echo $RESPONSE_MIXTE_CASH_TRANSFER | jq -r '.sale.id')
pay_sale $SALE_ID_MIXTE_CASH_TRANSFER '[ 
  {"amount": 15.0, "payment_method": "CASH", "amount_received": 15.0},
  {
    "amount": 15.0,
    "payment_method": "TRANSFER",
    "payment_details": {
      "operator": "Orange",
      "phone_number": "+237699001122"
    }
  }
]'

# Vente avec paiement MIXTE CASH + CARD
echo "----------------------------------------"
echo "🛒 Vente avec paiement MIXTE CASH + CARD"
RESPONSE_MIXTE_CASH_CARD=$(curl -s -X POST $BASE_URL/ \
-H "$HEADER" \
-d '{
  "cashier_id": 1,
  "notes": "Vente CASH+CARD",
  "items": [{"product_id": 205, "quantity": 1, "unit_price": 25.0}]
}')
SALE_ID_MIXTE_CASH_CARD=$(echo $RESPONSE_MIXTE_CASH_CARD | jq -r '.sale.id')
pay_sale $SALE_ID_MIXTE_CASH_CARD '[ 
  {"amount": 10.0, "payment_method": "CASH", "amount_received": 10.0},
  {"amount": 15.0, "payment_method": "CARD"}
]'

# Vente avec paiement MIXTE TRANSFER + CARD
echo "----------------------------------------"
echo "🛒 Vente avec paiement MIXTE TRANSFER + CARD"
RESPONSE_MIXTE_TRANSFER_CARD=$(curl -s -X POST $BASE_URL/ \
-H "$HEADER" \
-d '{
  "cashier_id": 1,
  "notes": "Vente TRANSFER+CARD",
  "items": [{"product_id": 206, "quantity": 2, "unit_price": 12.5}]
}')
SALE_ID_MIXTE_TRANSFER_CARD=$(echo $RESPONSE_MIXTE_TRANSFER_CARD | jq -r '.sale.id')
pay_sale $SALE_ID_MIXTE_TRANSFER_CARD '[ 
  {
    "amount": 10.0,
    "payment_method": "TRANSFER",
    "payment_details": {
      "operator": "Moov",
      "phone_number": "+237655443322"
    }
  },
  {"amount": 15.0, "payment_method": "CARD"}
]'

# Vente avec UN SEUL PRODUIT
echo "----------------------------------------"
echo "🛒 Vente avec UN SEUL PRODUIT"
RESPONSE_SINGLE_PRODUCT=$(curl -s -X POST $BASE_URL/ \
-H "$HEADER" \
-d '{
  "cashier_id": 1,
  "notes": "Vente 1 seul produit",
  "items": [{"product_id": 207, "quantity": 1, "unit_price": 9.99}]
}')
SALE_ID_SINGLE_PRODUCT=$(echo $RESPONSE_SINGLE_PRODUCT | jq -r '.sale.id')
pay_sale $SALE_ID_SINGLE_PRODUCT '[{"amount": 9.99, "payment_method": "CASH", "amount_received": 9.99}]'

# Affichage de toutes les ventes
echo "----------------------------------------"
echo "📋 Affichage de toutes les ventes..."
ALL_SALES=$(curl -s $BASE_URL/)
echo "$ALL_SALES" | jq
