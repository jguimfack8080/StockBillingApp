from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

class MovementType(str, Enum):
    IN = "IN"
    OUT = "OUT"

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

    class Config:
        orm_mode = True

class ProductBase(BaseModel):
    article_number: Optional[str] = None
    name: str
    description: Optional[str] = None
    price: float
    quantity: int = 0

class ProductCreate(ProductBase):
    category_ids: Optional[List[int]] = None

class ProductUpdate(ProductBase):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    category_ids: Optional[List[int]] = None

class Product(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    categories: List[Category] = []

    class Config:
        orm_mode = True

class StockMovementBase(BaseModel):
    product_id: int
    quantity: int
    movement_type: MovementType
    reason: Optional[str] = None

class StockMovementCreate(StockMovementBase):
    pass

class StockMovement(StockMovementBase):
    id: int
    created_at: datetime
    created_by: Optional[int] = None
    product: Product

    class Config:
        orm_mode = True 