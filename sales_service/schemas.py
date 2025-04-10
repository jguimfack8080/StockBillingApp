from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class PaymentMethod(str, Enum):
    CASH = "CASH"
    CARD = "CARD"
    TRANSFER = "TRANSFER"

class TransactionStatus(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"

class CustomerBase(BaseModel):
    first_name: str
    last_name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class SaleItemBase(BaseModel):
    product_id: int
    quantity: int
    unit_price: float

    def calculate_total(self) -> float:
        return self.quantity * self.unit_price

class SaleItemCreate(SaleItemBase):
    pass

class SaleItem(SaleItemBase):
    id: int
    sale_id: int
    total_price: float
    created_at: datetime

    class Config:
        from_attributes = True

class TransactionBase(BaseModel):
    amount: float
    payment_method: PaymentMethod
    payment_details: Optional[str] = None
    amount_received: Optional[float] = None
    change_amount: Optional[float] = None

    def calculate_change(self) -> float:
        if self.amount_received is not None and self.payment_method == PaymentMethod.CASH:
            return self.amount_received - self.amount
        return 0.0

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int
    sale_id: int
    status: TransactionStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class SaleBase(BaseModel):
    cashier_id: int
    customer_id: Optional[int] = None
    payment_method: PaymentMethod
    notes: Optional[str] = None

class SaleCreate(SaleBase):
    items: List[SaleItemCreate]
    transactions: List[TransactionCreate]

    def calculate_total(self) -> float:
        return sum(item.calculate_total() for item in self.items)

class SaleUpdate(BaseModel):
    status: Optional[TransactionStatus] = None
    payment_method: Optional[PaymentMethod] = None
    notes: Optional[str] = None

class Sale(SaleBase):
    id: int
    sale_number: str
    total_amount: float
    status: TransactionStatus
    created_at: datetime
    updated_at: datetime
    items: List[SaleItem] = []
    transactions: List[Transaction] = []

    class Config:
        from_attributes = True

class SaleResponse(BaseModel):
    sale: Sale
    change_amount: float
    items_count: int
    total_amount: float
    payment_status: str

class BulkSaleItem(SaleItemCreate):
    pass

class BulkSaleCreate(BaseModel):
    payment_method: PaymentMethod
    items: List[BulkSaleItem]
    transactions: List[TransactionCreate]

class BulkSalesCreate(BaseModel):
    cashier_id: int
    customer_id: Optional[int] = None
    sales: List[BulkSaleCreate]
