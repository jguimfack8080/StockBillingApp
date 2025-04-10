from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import os
from dotenv import load_dotenv

import models, schemas
from database import engine, get_db
from routers import sales, transactions, customers

# Load environment variables
load_dotenv()

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sales Service",
    description="API for managing sales, transactions, and customers",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(sales.router, prefix="/sales", tags=["sales"])
app.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
app.include_router(customers.router, prefix="/customers", tags=["customers"])

@app.get("/")
async def root():
    return {"message": "Sales Service is running"}
