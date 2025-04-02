from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    birth_date: date
    id_card_number: Optional[str] = None
    email: EmailStr
    password: str
    role: str  # admin / manager / caissier

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

class Token(BaseModel):
    access_token: str
    token_type: str
