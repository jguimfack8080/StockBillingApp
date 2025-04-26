import requests
from fastapi import HTTPException, status
from typing import Optional, Dict

class AuthService:
    def __init__(self, auth_service_url: str):
        self.auth_service_url = auth_service_url

    def get_current_user(self, token: str) -> Dict:
        """
        Récupère et valide les informations de l'utilisateur connecté depuis le service d'authentification.
        """
        try:
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(f"{self.auth_service_url}/users/me", headers=headers)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication credentials"
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Error fetching user information"
                )
        except requests.exceptions.RequestException as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Authentication service is unavailable"
            )

    def validate_token(self, token: str) -> bool:
        """
        Valide le token JWT auprès du service d'authentification.
        """
        try:
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(f"{self.auth_service_url}/users/me", headers=headers)
            return response.status_code == 200
        except:
            return False 