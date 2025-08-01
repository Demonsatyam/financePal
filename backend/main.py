from fastapi import FastAPI
import logging
import sys
from contextlib import asynccontextmanager

# --- Database Imports ---
# Import the central Base and engine objects
from database.db import Base, engine
# This import is CRITICAL. It ensures that Python loads the models.py file,
# which causes the User, Policy, etc. classes to be registered with the Base metadata.
from database import models

# --- Route Imports ---
from routes import auth, policy

# Configure logging to print to the console
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    This function manages application startup and shutdown events.
    """
    logging.info("Application startup...")
    logging.info("Connecting to the database and creating tables if they don't exist...")
    
    # Create all tables stored in the Base.metadata.
    # The 'checkfirst=True' argument prevents errors if the tables already exist.
    Base.metadata.create_all(bind=engine, checkfirst=True)
    
    logging.info("Database tables check/creation complete.")
    yield
    # Code below yield runs on application shutdown
    logging.info("Application shutdown.")

# Create the FastAPI app instance and attach the lifespan manager
app = FastAPI(lifespan=lifespan)

# Include the API routers from your routes files
app.include_router(auth.router)
app.include_router(policy.router)

@app.get("/")
def read_root():
    return {"status": "FinancePal API is running"}