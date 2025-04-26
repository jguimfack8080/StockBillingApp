from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import get_db
from middleware.auth import get_current_user, check_role_privileges
from utils import check_access, TRANSACTIONS_ACCESS

router = APIRouter()

@router.post("/", response_model=schemas.Transaction)
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    db_transaction = models.Transaction(
        sale_id=transaction.sale_id,
        amount=transaction.amount,
        payment_method=transaction.payment_method,
        payment_details=transaction.payment_details,
        status=models.TransactionStatus.PENDING
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def check_transactions_access(current_user: dict):
    allowed_roles = ["admin", "manager", "cashier"]
    if current_user["role"] not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès non autorisé. Seuls les administrateurs, managers et caissiers peuvent accéder à cette ressource."
        )

@router.get("/", response_model=List[schemas.Transaction])
def get_transactions(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    check_access(current_user, TRANSACTIONS_ACCESS, "transactions")
    
    transactions = db.query(models.Transaction).offset(skip).limit(limit).all()
    return transactions

@router.get("/sale/{sale_id}", response_model=List[schemas.Transaction])
def get_sale_transactions(
    sale_id: int, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    check_access(current_user, TRANSACTIONS_ACCESS, "transactions")
    
    transactions = db.query(models.Transaction).filter(models.Transaction.sale_id == sale_id).all()
    return transactions

@router.get("/{transaction_id}", response_model=schemas.Transaction)
def get_transaction(
    transaction_id: int, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    check_access(current_user, TRANSACTIONS_ACCESS, "transactions")
    
    transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

@router.put("/{transaction_id}/status", response_model=schemas.Transaction)
def update_transaction_status(
    transaction_id: int,
    status: schemas.TransactionStatus,
    db: Session = Depends(get_db)
):
    db_transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")

    db_transaction.status = status
    db.commit()
    db.refresh(db_transaction)
    return db_transaction 