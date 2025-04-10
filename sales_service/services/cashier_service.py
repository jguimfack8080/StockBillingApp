import requests
from sqlalchemy.orm import Session
import models
from typing import Optional

class CashierService:
    def __init__(self, auth_service_url: str):
        self.auth_service_url = auth_service_url

    def get_cashier_info(self, cashier_id: int) -> Optional[dict]:
        """Récupère les informations du caissier depuis le service d'authentification"""
        try:
            response = requests.get(f"{self.auth_service_url}/users/{cashier_id}")
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Erreur lors de la récupération des informations du caissier: {e}")
            return None

    def update_sale_cashier_info(self, db: Session, sale: models.Sale):
        """Met à jour les informations du caissier pour une vente"""
        cashier_info = self.get_cashier_info(sale.cashier_id)
        if cashier_info:
            sale.update_cashier_info(
                first_name=cashier_info["first_name"],
                last_name=cashier_info["last_name"]
            )
            db.commit()

    def update_all_sales_cashier_info(self, db: Session):
        """Met à jour les informations des caissiers pour toutes les ventes"""
        sales = db.query(models.Sale).filter(models.Sale.cashier_name.is_(None)).all()
        for sale in sales:
            self.update_sale_cashier_info(db, sale) 