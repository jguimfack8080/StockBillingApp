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
        payment_method=sale.payment_method,
        status=models.TransactionStatus.PENDING,
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

    # Créer les transactions
    change_amount = 0.0
    for transaction in sale.transactions:
        if transaction.payment_method == models.PaymentMethod.CASH:
            change_amount = transaction.calculate_change()
        
        db_transaction = models.Transaction(
            sale_id=db_sale.id,
            amount=transaction.amount,
            payment_method=transaction.payment_method,
            payment_details=transaction.payment_details,
            amount_received=transaction.amount_received,
            change_amount=change_amount,
            status=models.TransactionStatus.PENDING
        )
        db.add(db_transaction)

    db.commit()
    db.refresh(db_sale)

    # Préparer la réponse
    items_count = len(sale.items)
    payment_status = "completed" if change_amount >= 0 else "pending"

    return schemas.SaleResponse(
        sale=db_sale,
        change_amount=change_amount,
        items_count=items_count,
        total_amount=total_amount,
        payment_status=payment_status
    )

@router.post("/bulk", response_model=List[schemas.SaleResponse])
def create_bulk_sales(bulk_sale: schemas.BulkSaleCreate, db: Session = Depends(get_db)):
    created_sales = []
    
    for sale in bulk_sale.sales:
        # Définir le customer_id pour toutes les ventes si fourni dans bulk_sale
        if bulk_sale.customer_id:
            sale.customer_id = bulk_sale.customer_id
        sale.cashier_id = bulk_sale.cashier_id
        
        # Créer chaque vente individuellement
        created_sale = create_sale(sale, db)
        created_sales.append(created_sale)
    
    return created_sales

@router.get("/", response_model=List[schemas.Sale])
def get_sales(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    sales = db.query(models.Sale).offset(skip).limit(limit).all()
    return sales

@router.get("/{sale_id}", response_model=schemas.SaleResponse)
def get_sale(sale_id: int, db: Session = Depends(get_db)):
    sale = db.query(models.Sale).filter(models.Sale.id == sale_id).first()
    if sale is None:
        raise HTTPException(status_code=404, detail="Sale not found")
    
    # Calculer les métriques pour la réponse
    items_count = len(sale.items)
    total_amount = sale.total_amount
    change_amount = sale.transactions[0].change_amount if sale.transactions else 0.0
    payment_status = "completed" if all(t.status == models.TransactionStatus.COMPLETED for t in sale.transactions) else "pending"
    
    return schemas.SaleResponse(
        sale=sale,
        change_amount=change_amount,
        items_count=items_count,
        total_amount=total_amount,
        payment_status=payment_status
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
    
    return schemas.SaleResponse(
        sale=sale,
        change_amount=change_amount,
        items_count=items_count,
        total_amount=total_amount,
        payment_status=payment_status
    )

@router.put("/{sale_id}", response_model=schemas.SaleResponse)
def update_sale(sale_id: int, sale_update: schemas.SaleUpdate, db: Session = Depends(get_db)):
    db_sale = db.query(models.Sale).filter(models.Sale.id == sale_id).first()
    if db_sale is None:
        raise HTTPException(status_code=404, detail="Sale not found")

    if sale_update.status:
        db_sale.status = sale_update.status
    if sale_update.payment_method:
        db_sale.payment_method = sale_update.payment_method
    if sale_update.notes:
        db_sale.notes = sale_update.notes

    db.commit()
    db.refresh(db_sale)
    
    # Calculer les métriques pour la réponse
    items_count = len(db_sale.items)
    total_amount = db_sale.total_amount
    change_amount = db_sale.transactions[0].change_amount if db_sale.transactions else 0.0
    payment_status = "completed" if all(t.status == models.TransactionStatus.COMPLETED for t in db_sale.transactions) else "pending"
    
    return schemas.SaleResponse(
        sale=db_sale,
        change_amount=change_amount,
        items_count=items_count,
        total_amount=total_amount,
        payment_status=payment_status
    )
