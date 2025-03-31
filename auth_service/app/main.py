from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, users
from app.database import engine, SessionLocal
from app.models import User
from app.utils.security import get_password_hash
from app.utils.config import settings

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

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])

@app.on_event("startup")
def create_first_admin():
    # Connexion à la base de données
    db = SessionLocal()

    # Vérifie si un utilisateur admin existe déjà
    existing_admin = db.query(User).filter(User.role == "admin").first()
    if not existing_admin:
        # Si aucun utilisateur admin n'existe, on le crée
        hashed_password = get_password_hash("adminpassword")  # Choisis un mot de passe sécurisé
        new_admin = User(
            email="admin@test.com",
            hashed_password=hashed_password,
            role="admin"
        )
        
        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)
        print(f"Utilisateur admin créé : {new_admin.email}")

@app.get("/")
def health_check():
    return {"status": "OK", "security": "ACTIVE"}
