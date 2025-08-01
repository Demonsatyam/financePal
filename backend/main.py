from fastapi import FastAPI
import logging
import sys
from contextlib import asynccontextmanager

# --- Database Imports ---
# Import the central Base, AdminBase, and engine objects
from database.db import Base, AdminBase, engine
# This import is CRITICAL. It ensures that Python loads the models files,
# which causes all model classes to be registered with their respective Base metadata.
from database import models
from database.admin import admin_models

# --- Route Imports ---
from routes import auth, policy
from routes import admin  # Your new admin router

# Configure logging to print to the console
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    This function manages application startup and shutdown events.
    It's the recommended way to handle setup/teardown logic.
    """
    logging.info("Application startup...")
    logging.info("Connecting to the database and creating tables if they don't exist...")
    
    # Create all tables stored in the Base and AdminBase metadata.
    # The 'checkfirst=True' would also work, but since we have a solid reset
    # script, create_all is fine.
    Base.metadata.create_all(bind=engine)
    AdminBase.metadata.create_all(bind=engine)
    
    logging.info("Database tables check/creation complete.")
    yield
    # Code below yield runs on application shutdown
    logging.info("Application shutdown.")

# Create the FastAPI app instance and attach the lifespan manager
app = FastAPI(lifespan=lifespan)

# --- Include API Routers ---
# This makes the endpoints from your route files available in the app.
# Using a prefix helps organize URLs (e.g., /admin/policies).
# Using tags groups the endpoints neatly in the API docs.

app.include_router(auth.router, prefix="/user", tags=["User Authentication"])
app.include_router(policy.router, prefix="/user", tags=["User Policies"])
app.include_router(admin.router, prefix="/admin", tags=["Admin Management"])

@app.get("/", tags=["Root"])
def read_root():
    """
    A simple endpoint to confirm the API is running.
    """
    return {"status": "FinancePal API is running"}