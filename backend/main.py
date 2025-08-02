from fastapi import FastAPI
import logging
import sys
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import os

# --- Load environment variables ---
load_dotenv()  # Automatically loads from .env in the same directory

# --- Environment Variable Access ---
DATABASE_URL = os.getenv("DATABASE_URL")
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
REGION = os.getenv("GOOGLE_CLOUD_LOCATION")
USE_VERTEX_AI = os.getenv("GOOGLE_GENAI_USE_VERTEXAI") == "True"

# --- Database Imports ---
from database.db import Base, AdminBase, engine
from database import models
from database.admin import admin_models

# --- Route Imports ---
from routes import auth, policy
from routes import admin  # Admin router only

# --- Logging Setup ---
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

    # Debug: print loaded environment variables
    logging.info(f"GOOGLE_CLOUD_PROJECT: {PROJECT_ID}")
    logging.info(f"GOOGLE_CLOUD_LOCATION: {REGION}")
    logging.info(f"Vertex AI Enabled: {USE_VERTEX_AI}")

    yield
    logging.info("Application shutdown.")

# --- FastAPI App Init ---
app = FastAPI(lifespan=lifespan)

# --- Routers ---
app.include_router(auth.router, prefix="/user", tags=["User Authentication"])
app.include_router(policy.router, prefix="/user", tags=["User Policies"])
app.include_router(admin.router, prefix="/admin", tags=["Admin Management"])

@app.get("/", tags=["Root"])
def read_root():
    return {"status": "FinancePal API is running"}
