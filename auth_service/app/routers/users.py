from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from ..database import get_db
from ..models import User
from ..schemas import UserCreate, UserOut, DeactivationReason
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


# Endpoint pour créer un utilisateur (réservé aux administrateurs)
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
    if user.birth_date > datetime.today().date():
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

@router.put("/deactivate/{user_id}", tags=["users"])
def deactivate_user(
    user_id: int,
    reason: DeactivationReason,  # La raison est passée dans le corps de la requête
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # Vérification des privilèges d'accès : seul un admin peut désactiver un utilisateur
    check_admin_privileges(current_user)
    
    # Recherche de l'utilisateur
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if user.is_active:
        # Désactivation de l'utilisateur et ajout de la raison
        user.is_active = False
        user.deactivation_date = datetime.utcnow()  # Enregistrer la date de désactivation
        user.deactivation_reason = reason.reason  # Ajouter la raison de la désactivation
        message = f"User {user_id} has been deactivated for the following reason: {reason.reason}"
    else:
        # Réactivation de l'utilisateur
        user.is_active = True
        user.deactivation_date = None
        user.deactivation_reason = None
        message = f"User {user_id} has been reactivated"

    db.commit()
    db.refresh(user)

    return {"message": message}
