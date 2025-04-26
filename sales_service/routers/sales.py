from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import get_db
from services.cashier_service import CashierService
from middleware.auth import get_current_user
from utils import check_access, SALES_ACCESS
import os
from datetime import datetime

router = APIRouter()
cashier_service = CashierService(os.getenv("AUTH_SERVICE_URL", "http://auth_service:8001"))

@router.post("/", response_model=schemas.SaleResponse)
def create_sale(
    sale: schemas.SaleCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    check_access(current_user, SALES_ACCESS, "ventes")
    
    # Vérifier que le client existe
    if sale.customer_id:
        customer = db.query(models.Customer).filter(models.Customer.id == sale.customer_id).first()
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Client avec l'ID {sale.customer_id} n'existe pas"
            )
    
    # Calculer le total automatiquement
    total_amount = sale.calculate_total()
    
    # Générer un ID temporaire pour le numéro de vente
    last_sale = db.query(models.Sale).order_by(models.Sale.id.desc()).first()
    next_id = (last_sale.id + 1) if last_sale else 1
    date_str = datetime.now().strftime("%Y%m%d")
    sale_number = f"V{date_str}-{next_id:05d}"
    
    # Créer la vente avec le numéro généré et l'ID du caissier connecté
    db_sale = models.Sale(
        sale_number=sale_number,
        cashier_id=current_user["id"],  # Utiliser l'ID de l'utilisateur connecté
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
        id=db_sale.id,
        sale_number=db_sale.sale_number,
        customer_id=db_sale.customer_id,
        cashier_id=db_sale.cashier_id,
        total_amount=total_amount,
        status=db_sale.status,
        notes=db_sale.notes,
        created_at=db_sale.created_at,
        items_count=items_count,
        payment_status="pending",
        remaining_amount=remaining_amount,
        change_amount=0.0
    )

@router.post("/{sale_id}/pay", response_model=schemas.SaleResponse)
def process_payment(
    sale_id: int, 
    payment: schemas.SalePayment, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    check_access(current_user, SALES_ACCESS, "ventes")
    
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
        id=db_sale.id,
        sale_number=db_sale.sale_number,
        customer_id=db_sale.customer_id,
        cashier_id=db_sale.cashier_id,
        total_amount=db_sale.total_amount,
        status=db_sale.status,
        notes=db_sale.notes,
        created_at=db_sale.created_at,
        items_count=items_count,
        payment_status="completed",
        remaining_amount=remaining_amount,
        change_amount=total_change,
        transactions=[schemas.TransactionResponse.from_orm(t) for t in db_sale.transactions]
    )

@router.get("/", response_model=List[schemas.Sale])
def get_sales(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    check_access(current_user, SALES_ACCESS, "ventes")
    
    # Si l'utilisateur est un caissier, ne montrer que ses ventes
    if current_user["role"] == "cashier":
        sales = db.query(models.Sale).filter(models.Sale.cashier_id == current_user["id"]).offset(skip).limit(limit).all()
    else:
        sales = db.query(models.Sale).offset(skip).limit(limit).all()
    return sales

@router.get("/{sale_id}", response_model=schemas.SaleResponse)
def get_sale(
    sale_id: int, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    check_access(current_user, SALES_ACCESS, "ventes")
    
    db_sale = db.query(models.Sale).filter(models.Sale.id == sale_id).first()
    if db_sale is None:
        raise HTTPException(status_code=404, detail="Sale not found")
    return db_sale

@router.get("/number/{sale_number}", response_model=schemas.SaleResponse)
def get_sale_by_number(
    sale_number: str, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    check_access(current_user, SALES_ACCESS, "ventes")
    
    sale = db.query(models.Sale).filter(models.Sale.sale_number == sale_number).first()
    if sale is None:
        raise HTTPException(status_code=404, detail="Sale not found")
    return sale

@router.put("/{sale_id}", response_model=schemas.SaleResponse)
def update_sale(
    sale_id: int, 
    sale_update: schemas.SaleUpdate, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    check_access(current_user, SALES_ACCESS, "ventes")
    
    db_sale = db.query(models.Sale).filter(models.Sale.id == sale_id).first()
    if db_sale is None:
        raise HTTPException(status_code=404, detail="Sale not found")

    if sale_update.status:
        db_sale.status = sale_update.status
        # Si la vente est annulée, mettre à jour le statut des transactions
        if sale_update.status == models.SaleStatus.CANCELLED:
            for transaction in db_sale.transactions:
                transaction.status = models.TransactionStatus.REFUNDED
                transaction.payment_details = {
                    "refund_date": datetime.utcnow().isoformat(),
                    "refund_reason": "Sale cancelled"
                }
    if sale_update.notes:
        db_sale.notes = sale_update.notes

    db.commit()
    db.refresh(db_sale)

    # Calculer les valeurs requises pour la réponse
    items_count = len(db_sale.items)
    remaining_amount = db_sale.calculate_remaining_amount()
    total_change = sum(t.change_amount or 0 for t in db_sale.transactions)
    payment_status = "completed" if db_sale.status == models.SaleStatus.COMPLETED else "pending"

    return schemas.SaleResponse(
        id=db_sale.id,
        sale_number=db_sale.sale_number,
        customer_id=db_sale.customer_id,
        cashier_id=db_sale.cashier_id,
        total_amount=db_sale.total_amount,
        status=db_sale.status,
        notes=db_sale.notes,
        created_at=db_sale.created_at,
        items_count=items_count,
        payment_status=payment_status,
        remaining_amount=remaining_amount,
        change_amount=total_change,
        transactions=[schemas.TransactionResponse.from_orm(t) for t in db_sale.transactions]
    )
