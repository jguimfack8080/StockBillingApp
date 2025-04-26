from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import requests
import os

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Vérifier l'utilisateur auprès du service d'authentification
    auth_service_url = os.getenv("AUTH_SERVICE_URL", "http://auth_service:8000")
    response = requests.get(
        f"{auth_service_url}/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if response.status_code != 200:
        raise credentials_exception
    
    return response.json()

def get_current_active_user(current_user = Depends(get_current_user)):
    if not current_user.get("is_active"):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def get_current_admin_user(current_user = Depends(get_current_active_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
    return current_user 