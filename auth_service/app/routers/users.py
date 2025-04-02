from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date
from ..database import get_db
from ..models import User
from ..schemas import UserCreate, UserOut
from ..utils.security import get_password_hash, check_admin_privileges
from ..dependencies import get_current_user

router = APIRouter()

ALLOWED_ROLES = ["admin", "manager", "cashier"]

# Endpoint pour récupérer tous les utilisateurs, réservé aux administrateurs
@router.get("/", response_model=list[UserOut], tags=["users"])
def get_users(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # Vérification des privilèges d'accès : seul un admin peut voir la liste des utilisateurs
    check_admin_privileges(current_user)
    
    # Récupérer la liste des utilisateurs
    users = db.query(User).all()
    return users


@router.post("/", response_model=UserOut)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # Vérification des privilèges d'accès : seul un admin peut créer un compte
    check_admin_privileges(current_user)
    
    # Vérification que le rôle fourni est autorisé
    if user.role not in ALLOWED_ROLES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid role. Allowed roles: {', '.join(ALLOWED_ROLES)}"
        )
    
    # Vérification que les champs obligatoires ne sont pas vides
    if not user.first_name or not user.last_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="First name and last name are required"
        )
    
    # Vérification de la date de naissance (ne peut être dans le futur)
    if user.birth_date > date.today():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Birth date cannot be in the future"
        )
    
    # Vérification de la présence du numéro de carte d'identité
    if not user.id_card_number:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID card number is required"
        )
    
    # Vérification de l'unicité de l'email
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already in use"
        )
    
    # Vérification de l'unicité du numéro de carte d'identité
    existing_id_card = db.query(User).filter(User.id_card_number == user.id_card_number).first()
    if existing_id_card:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID card number already in use"
        )
    
    # Tentative de création de l'utilisateur
    try:
        hashed_password = get_password_hash(user.password)
        role_value = user.role.value if hasattr(user.role, "value") else user.role
        db_user = User(
            first_name=user.first_name,
            last_name=user.last_name,
            birth_date=user.birth_date,
            id_card_number=user.id_card_number,
            email=user.email,
            hashed_password=hashed_password,
            role=role_value,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return UserOut.from_orm(db_user)
    except Exception as e:
        # En développement, renvoyer l'exception complète pour faciliter le débogage
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )
