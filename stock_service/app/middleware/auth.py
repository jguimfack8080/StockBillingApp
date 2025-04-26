from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional, Dict
import os
import requests
from dotenv import load_dotenv

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# Configuration du service d'authentification
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://auth_service:8000")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict:
    """
    Middleware pour récupérer et valider les informations de l'utilisateur connecté
    en utilisant le service d'authentification.
    """
    try:
        # Vérifier le token auprès du service d'authentification
        response = requests.get(
            f"{AUTH_SERVICE_URL}/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )
            
        user_data = response.json()
        return {
            "id": user_data["id"],
            "role": user_data["role"]
        }
    except Exception:
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