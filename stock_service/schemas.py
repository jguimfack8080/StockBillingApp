from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class ProductStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DISCONTINUED = "discontinued"

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    quantity: int = 0
    status: ProductStatus = ProductStatus.ACTIVE

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    status: Optional[ProductStatus] = None

class Product(ProductBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
