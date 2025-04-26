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

class SaleStatus(str, Enum):
    DRAFT = "DRAFT"  # Vente créée mais non payée
    PENDING = "PENDING"  # En attente de paiement
    COMPLETED = "COMPLETED"  # Paiement effectué
    CANCELLED = "CANCELLED"  # Vente annulée

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

class SaleItemCreate(BaseModel):
    product_id: int
    quantity: int
    unit_price: float

    def calculate_total(self) -> float:
        return self.quantity * self.unit_price

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
    payment_details: Optional[Dict[str, Any]] = None
    amount_received: Optional[float] = None
    change_amount: Optional[float] = None

    def calculate_change(self) -> float:
        if self.amount_received is not None and self.payment_method == PaymentMethod.CASH:
            return self.amount_received - self.amount
        return 0.0

class TransactionCreate(TransactionBase):
    pass  # On retire le sale_id car il sera fourni automatiquement

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
    notes: Optional[str] = None

class SaleCreate(BaseModel):
    customer_id: int
    items: List[SaleItemCreate]
    notes: Optional[str] = None

    def calculate_total(self) -> float:
        return sum(item.calculate_total() for item in self.items)

class SalePayment(BaseModel):
    transactions: List[TransactionCreate]

    def validate_payment(self, total_amount: float) -> bool:
        total_paid = sum(t.amount for t in self.transactions)
        return abs(total_paid - total_amount) < 0.01  # Tolérance pour les arrondis

class SaleUpdate(BaseModel):
    status: Optional[str] = Field(None, description="Nouveau statut de la vente")
    notes: Optional[str] = Field(None, description="Notes supplémentaires")

    class Config:
        from_attributes = True
        extra = "allow"  # Permet des champs supplémentaires

class Sale(SaleBase):
    id: int
    sale_number: str
    total_amount: float
    status: SaleStatus
    created_at: datetime
    updated_at: datetime
    items: List[SaleItem] = []
    transactions: List[Transaction] = []

    class Config:
        from_attributes = True

class TransactionResponse(BaseModel):
    id: int
    amount: float
    payment_method: PaymentMethod
    status: TransactionStatus
    payment_details: Optional[Dict[str, Any]] = None
    amount_received: Optional[float] = None
    change_amount: Optional[float] = None
    mixed_payments: Optional[List[Dict[str, Any]]] = None  # Détails de tous les moyens de paiement
    created_at: datetime

    class Config:
        from_attributes = True

class SaleResponse(BaseModel):
    id: int
    sale_number: str
    customer_id: int
    cashier_id: int
    total_amount: float
    status: str
    notes: Optional[str]
    created_at: datetime
    items_count: int
    payment_status: str
    remaining_amount: float
    change_amount: float
    transactions: List[TransactionResponse] = []

    class Config:
        from_attributes = True

class BulkSaleCreate(BaseModel):
    items: List[SaleItemCreate]

class BulkSalesCreate(BaseModel):
    cashier_id: int
    customer_id: Optional[int] = None
    sales: List[BulkSaleCreate]
