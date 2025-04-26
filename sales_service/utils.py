from fastapi import HTTPException, status
from typing import List

def check_access(current_user: dict, allowed_roles: List[str], resource_name: str):
    """Vérifie si l'utilisateur a accès à une ressource spécifique"""
    if current_user["role"] not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Accès non autorisé. Seuls les {', '.join(allowed_roles)} peuvent accéder à cette ressource."
        )

# Constantes pour les rôles autorisés
SALES_ACCESS = ["admin", "manager", "cashier"]
CUSTOMERS_ACCESS = ["admin", "manager", "cashier"]
TRANSACTIONS_ACCESS = ["admin", "manager", "cashier"] 