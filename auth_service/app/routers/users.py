from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..schemas import UserCreate, UserOut
from ..utils.security import get_password_hash
from ..dependencies import get_current_user

router = APIRouter()

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..schemas import UserCreate, UserOut
from ..utils.security import get_password_hash
from ..dependencies import get_current_user

router = APIRouter()

@router.post("/", response_model=UserOut)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    print(f"Attempt to create: {user.email} by {current_user}")

    if current_user.get("role") != "admin":
        print("Access denied: User is not admin")
        raise HTTPException(status_code=403, detail="Access denied")
    
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        print(f"Email already in use: {user.email}")
        raise HTTPException(status_code=400, detail="Email already in use")
    
    try:
        hashed_password = get_password_hash(user.password)
        db_user = User(
            email=user.email,
            hashed_password=hashed_password,
            role=user.role if hasattr(user, "role") else "cashier"
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        print(f"User successfully created: {db_user.email}")
        
        return UserOut(email=db_user.email, role=db_user.role)  # ✅ Only return necessary data
    except Exception as e:
        print(f"Error during creation: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
