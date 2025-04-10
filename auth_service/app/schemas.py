from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional

# Existing schemas
class UserCreate(BaseModel):
    first_name: str
    last_name: str
    birth_date: date
    id_card_number: Optional[str] = None
    email: EmailStr
    password: str
    role: str  # admin / manager / cashier

class UserOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    birth_date: date
    id_card_number: Optional[str]
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True

# New schema for user update
class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birth_date: Optional[date] = None
    id_card_number: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None  # admin / manager / cashier
    is_active: Optional[bool] = None

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class DeactivationReason(BaseModel):
    reason: str
