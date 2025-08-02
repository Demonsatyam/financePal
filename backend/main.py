from fastapi import FastAPI
import logging
import sys
from contextlib import asynccontextmanager

# --- Database Imports ---
from database.db import Base, AdminBase, engine
from database import models
from database.admin import admin_models

# --- Route Imports ---
from routes import auth, policy
from routes import admin  # Admin router only

# Configure logging to print to the console
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    This function manages application startup and shutdown events.
    """
    logging.info("Application startup...")
    logging.info("Connecting to the database and creating tables if they don't exist...")
    
    Base.metadata.create_all(bind=engine)
    AdminBase.metadata.create_all(bind=engine)
    
    logging.info("Database tables check/creation complete.")
    yield
    logging.info("Application shutdown.")

app = FastAPI(lifespan=lifespan)

# Include only non-agent routers
app.include_router(auth.router, prefix="/user", tags=["User Authentication"])
app.include_router(policy.router, prefix="/user", tags=["User Policies"])
app.include_router(admin.router, prefix="/admin", tags=["Admin Management"])

@app.get("/", tags=["Root"])
def read_root():
    return {"status": "FinancePal API is running"}
