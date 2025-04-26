from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, users, update_user, me  # Import me router here
from app.database import engine, SessionLocal
from app.models import User
from app.utils.security import get_password_hash
from app.utils.config import settings
from datetime import datetime

# Créer les tables dans la base de données
from app.database import Base
Base.metadata.create_all(bind=engine)

# Création de l'application FastAPI
app = FastAPI()

# CORS (Ajuste pour la production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(update_user.router, prefix="/users", tags=["users"])
app.include_router(me.router, prefix="/users", tags=["users"])  # Add me router

@app.on_event("startup")
def create_first_admin():
    """Crée un compte administrateur au démarrage s'il n'existe pas encore."""
    db = SessionLocal()

    try:
        existing_admin = db.query(User).filter(User.role == "admin").first()
        if not existing_admin:
            hashed_password = get_password_hash("adminpassword")  # Remplace par un mot de passe sécurisé
            new_admin = User(
                first_name="Admin",
                last_name="User",
                birth_date="1990-01-01",  # Date fictive, à remplacer si nécessaire
                id_card_number=None,  # Optionnel
                email="admin@test.com",
                hashed_password=hashed_password,
                role="admin",
                created_at=datetime.utcnow()
            )

            db.add(new_admin)
            db.commit()
            db.refresh(new_admin)
            print(f"✅ Administrateur créé avec succès : {new_admin.email}")

    except Exception as e:
        print(f"❌ Erreur lors de la création de l'admin : {e}")
    finally:
        db.close()

@app.get("/")
def health_check():
    """Endpoint pour vérifier si l'API fonctionne bien."""
    return {"status": "OK", "security": "ACTIVE"}
