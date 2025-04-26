from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas
from ..dependencies import get_current_active_user, get_current_admin_user
from ..database import get_db

router = APIRouter(
    prefix="/stock-movements",
    tags=["stock-movements"]
)

@router.post("/", response_model=schemas.StockMovement)
def create_stock_movement(
    movement: schemas.StockMovementCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_user)
):
    # Vérifier si le produit existe
    product = db.query(models.Product).filter(models.Product.id == movement.product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Créer le mouvement de stock
    db_movement = models.StockMovement(
        product_id=movement.product_id,
        quantity=movement.quantity,
        movement_type=movement.movement_type,
        reason=movement.reason,
        created_by=current_user["id"]
    )
    
    # Mettre à jour la quantité du produit
    if movement.movement_type == schemas.MovementType.IN:
        product.quantity += movement.quantity
    else:  # OUT
        if product.quantity < movement.quantity:
            raise HTTPException(
                status_code=400,
                detail="Insufficient stock quantity"
            )
        product.quantity -= movement.quantity
    
    db.add(db_movement)
    db.commit()
    db.refresh(db_movement)
    return db_movement

@router.get("/", response_model=List[schemas.StockMovement])
def get_stock_movements(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    movements = db.query(models.StockMovement).offset(skip).limit(limit).all()
    return movements

@router.get("/product/{product_id}", response_model=List[schemas.StockMovement])
def get_product_stock_movements(
    product_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    # Vérifier si le produit existe
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    movements = (
        db.query(models.StockMovement)
        .filter(models.StockMovement.product_id == product_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return movements 