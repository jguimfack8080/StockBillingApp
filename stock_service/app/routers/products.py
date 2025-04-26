from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy.exc import IntegrityError

from .. import models, schemas
from ..dependencies import get_current_active_user, get_current_admin_user
from ..database import get_db

router = APIRouter(
    prefix="/products",
    tags=["products"]
)

@router.post("/", response_model=schemas.Product)
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_user)
):
    try:
        db_product = models.Product(
            article_number=product.article_number,
            name=product.name,
            description=product.description,
            price=product.price,
            quantity=product.quantity,
            created_by=current_user["id"],
            updated_by=current_user["id"]
        )
        
        # Ajouter les catégories si spécifiées
        if product.category_ids:
            categories = db.query(models.Category).filter(models.Category.id.in_(product.category_ids)).all()
            db_product.categories = categories
            
            # Enregistrer qui a fait l'association
            for category in categories:
                db.execute(
                    "INSERT INTO product_categories (product_id, category_id, created_by) VALUES (:product_id, :category_id, :created_by)",
                    {"product_id": db_product.id, "category_id": category.id, "created_by": current_user["id"]}
                )
        
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Un produit avec ce nom existe déjà"
        )

@router.get("/", response_model=List[schemas.Product])
def get_products(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    products = db.query(models.Product).offset(skip).limit(limit).all()
    return products

@router.get("/{product_id}", response_model=schemas.Product)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=schemas.Product)
def update_product(
    product_id: int,
    product_update: schemas.ProductUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_user)
):
    try:
        db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
        if db_product is None:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Mettre à jour les champs fournis
        for field, value in product_update.dict(exclude_unset=True).items():
            if field != "category_ids":
                setattr(db_product, field, value)
        
        # Mettre à jour l'utilisateur qui a modifié
        db_product.updated_by = current_user["id"]
        
        # Mettre à jour les catégories si spécifiées
        if product_update.category_ids is not None:
            # Supprimer les anciennes associations
            db.execute(
                "DELETE FROM product_categories WHERE product_id = :product_id",
                {"product_id": product_id}
            )
            
            # Ajouter les nouvelles associations
            categories = db.query(models.Category).filter(models.Category.id.in_(product_update.category_ids)).all()
            for category in categories:
                db.execute(
                    "INSERT INTO product_categories (product_id, category_id, created_by) VALUES (:product_id, :category_id, :created_by)",
                    {"product_id": product_id, "category_id": category.id, "created_by": current_user["id"]}
                )
        
        db.commit()
        db.refresh(db_product)
        return db_product
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Un produit avec ce nom existe déjà"
        )

@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_user)
):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted successfully"} 