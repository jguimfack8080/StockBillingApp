from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    birth_date = Column(String(10), nullable=False)  # Format YYYY-MM-DD
    id_card_number = Column(String(50), nullable=True)  # Optionnel
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    role = Column(String(50), nullable=False)  # admin / manager / caissier
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
