from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import products, categories, stock_movements
from .database import engine, Base

# Créer les tables de la base de données
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Stock Service",
    description="API pour la gestion des stocks",
    version="1.0.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure les routeurs
app.include_router(products.router)
app.include_router(categories.router)
app.include_router(stock_movements.router)

@app.get("/")
async def root():
    return {"message": "Stock Service API"} 