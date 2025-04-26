from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import get_db
from services.cashier_service import CashierService
import os
from datetime import datetime

router = APIRouter()
cashier_service = CashierService(os.getenv("AUTH_SERVICE_URL", "http://auth_service:8001"))

@router.post("/", response_model=schemas.SaleResponse)
def create_sale(sale: schemas.SaleCreate, db: Session = Depends(get_db)):
    # Calculer le total automatiquement
    total_amount = sale.calculate_total()
    
    # Générer un ID temporaire pour le numéro de vente
    last_sale = db.query(models.Sale).order_by(models.Sale.id.desc()).first()
    next_id = (last_sale.id + 1) if last_sale else 1
    date_str = datetime.now().strftime("%Y%m%d")
    sale_number = f"V{date_str}-{next_id:05d}"
    
    # Créer la vente avec le numéro généré
    db_sale = models.Sale(
        sale_number=sale_number,
        cashier_id=sale.cashier_id,
        customer_id=sale.customer_id,
        total_amount=total_amount,
        status=models.SaleStatus.DRAFT,
        notes=sale.notes
    )
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)

    # Mettre à jour les informations du caissier
    cashier_service.update_sale_cashier_info(db, db_sale)

    # Créer les articles de vente
    for item in sale.items:
        db_item = models.SaleItem(
            sale_id=db_sale.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=item.unit_price,
            total_price=item.calculate_total()
        )
        db.add(db_item)

    db.commit()
    db.refresh(db_sale)

    # Préparer la réponse
    items_count = len(sale.items)
    remaining_amount = db_sale.calculate_remaining_amount()

    return schemas.SaleResponse(
        sale=db_sale,
        change_amount=0.0,
        items_count=items_count,
        total_amount=total_amount,
        payment_status="pending",
        remaining_amount=remaining_amount
    )

@router.post("/{sale_id}/pay", response_model=schemas.SaleResponse)
def process_payment(sale_id: int, payment: schemas.SalePayment, db: Session = Depends(get_db)):
    db_sale = db.query(models.Sale).filter(models.Sale.id == sale_id).first()
    if db_sale is None:
        raise HTTPException(status_code=404, detail="Sale not found")

    if db_sale.status != models.SaleStatus.DRAFT:
        raise HTTPException(status_code=400, detail="Sale is not in draft status")

    if len(payment.transactions) > 2:
        raise HTTPException(status_code=400, detail="Maximum 2 payment methods allowed")

    if not payment.validate_payment(db_sale.total_amount):
        raise HTTPException(status_code=400, detail="Payment amount does not match sale total")

    # Créer les transactions
    total_change = 0.0
    for transaction in payment.transactions:
        if transaction.payment_method == models.PaymentMethod.CASH:
            change = transaction.calculate_change()
            total_change += change
        
        db_transaction = models.Transaction(
            sale_id=db_sale.id,
            amount=transaction.amount,
            payment_method=transaction.payment_method,
            payment_details=transaction.payment_details,
            amount_received=transaction.amount_received,
            change_amount=change if transaction.payment_method == models.PaymentMethod.CASH else 0.0,
            status=models.TransactionStatus.COMPLETED
        )
        db.add(db_transaction)

    # Mettre à jour le statut de la vente
    db_sale.status = models.SaleStatus.COMPLETED
    db.commit()
    db.refresh(db_sale)

    # Préparer la réponse
    items_count = len(db_sale.items)
    remaining_amount = db_sale.calculate_remaining_amount()

    return schemas.SaleResponse(
        sale=db_sale,
        change_amount=total_change,
        items_count=items_count,
        total_amount=db_sale.total_amount,
        payment_status="completed",
        remaining_amount=remaining_amount
    )

@router.get("/", response_model=List[schemas.Sale])
def get_sales(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    sales = db.query(models.Sale).offset(skip).limit(limit).all()
    return sales

@router.get("/{sale_id}", response_model=schemas.SaleResponse)
def get_sale(sale_id: int, db: Session = Depends(get_db)):
    db_sale = db.query(models.Sale).filter(models.Sale.id == sale_id).first()
    if db_sale is None:
        raise HTTPException(status_code=404, detail="Sale not found")

    items_count = len(db_sale.items)
    total_change = sum(t.change_amount or 0.0 for t in db_sale.transactions)
    remaining_amount = db_sale.calculate_remaining_amount()
    payment_status = "completed" if db_sale.is_paid() else "pending"

    return schemas.SaleResponse(
        sale=db_sale,
        change_amount=total_change,
        items_count=items_count,
        total_amount=db_sale.total_amount,
        payment_status=payment_status,
        remaining_amount=remaining_amount
    )

@router.get("/number/{sale_number}", response_model=schemas.SaleResponse)
def get_sale_by_number(sale_number: str, db: Session = Depends(get_db)):
    sale = db.query(models.Sale).filter(models.Sale.sale_number == sale_number).first()
    if sale is None:
        raise HTTPException(status_code=404, detail="Sale not found")
    
    # Calculer les métriques pour la réponse
    items_count = len(sale.items)
    total_amount = sale.total_amount
    change_amount = sale.transactions[0].change_amount if sale.transactions else 0.0
    payment_status = "completed" if all(t.status == models.TransactionStatus.COMPLETED for t in sale.transactions) else "pending"
    remaining_amount = sale.calculate_remaining_amount()
    
    return schemas.SaleResponse(
        sale=sale,
        change_amount=change_amount,
        items_count=items_count,
        total_amount=total_amount,
        payment_status=payment_status,
        remaining_amount=remaining_amount
    )

@router.put("/{sale_id}", response_model=schemas.SaleResponse)
def update_sale(sale_id: int, sale_update: schemas.SaleUpdate, db: Session = Depends(get_db)):
    db_sale = db.query(models.Sale).filter(models.Sale.id == sale_id).first()
    if db_sale is None:
        raise HTTPException(status_code=404, detail="Sale not found")

    # Si le statut est modifié
    if sale_update.status:
        # Si la vente est annulée, marquer toutes les transactions comme remboursées
        if sale_update.status == models.SaleStatus.CANCELLED:
            for transaction in db_sale.transactions:
                if transaction.status == models.TransactionStatus.COMPLETED:
                    transaction.status = models.TransactionStatus.REFUNDED
                    transaction.payment_details = {
                        **(transaction.payment_details or {}),
                        "refund_reason": "Sale cancelled",
                        "refund_date": datetime.now().isoformat()
                    }
        
        # Si la vente est marquée comme complétée, vérifier que toutes les transactions sont complétées
        elif sale_update.status == models.SaleStatus.COMPLETED:
            if not db_sale.is_paid():
                raise HTTPException(
                    status_code=400,
                    detail="Cannot mark sale as completed: payment is not complete"
                )
            for transaction in db_sale.transactions:
                if transaction.status == models.TransactionStatus.PENDING:
                    transaction.status = models.TransactionStatus.COMPLETED
        
        # Si la vente est marquée comme en attente, vérifier qu'elle n'est pas déjà payée
        elif sale_update.status == models.SaleStatus.PENDING:
            if db_sale.is_paid():
                raise HTTPException(
                    status_code=400,
                    detail="Cannot mark sale as pending: payment is already complete"
                )
        
        db_sale.status = sale_update.status

    # Mettre à jour les notes si fournies
    if sale_update.notes:
        db_sale.notes = sale_update.notes

    db.commit()
    db.refresh(db_sale)
    
    # Calculer les métriques pour la réponse
    items_count = len(db_sale.items)
    total_change = sum(t.change_amount or 0.0 for t in db_sale.transactions)
    remaining_amount = db_sale.calculate_remaining_amount()
    payment_status = "completed" if db_sale.is_paid() else "pending"
    
    return schemas.SaleResponse(
        sale=db_sale,
        change_amount=total_change,
        items_count=items_count,
        total_amount=db_sale.total_amount,
        payment_status=payment_status,
        remaining_amount=remaining_amount
    )
