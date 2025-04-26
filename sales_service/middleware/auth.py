from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional, Dict
import os
from services.auth_service import AuthService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# Créer une instance du service d'authentification
# En développement local, utilisez localhost:8001
# En production (Docker), utilisez auth_service:8000
auth_service_url = os.getenv("AUTH_SERVICE_URL", "http://localhost:8001")
auth_service = AuthService(auth_service_url)

async def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict:
    """
    Middleware pour récupérer et valider les informations de l'utilisateur connecté.
    """
    try:
        # Récupérer et valider les informations de l'utilisateur
        user = auth_service.get_current_user(token)
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

def check_role_privileges(current_user: Dict, required_role: str):
    """
    Vérifie si l'utilisateur a le rôle requis.
    """
    if current_user.get("role") != required_role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Access denied: {required_role} privileges required"
        ) 