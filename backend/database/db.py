from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")


DATABASE_URL = "postgresql://postgres:8762@localhost:5432/insurance_db"

# The engine is the connection source for the database
engine = create_engine(DATABASE_URL)

# SessionLocal is a factory for creating new database session objects
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is the declarative base class that our models will inherit from
Base = declarative_base()

# This dependency function will be imported by your API routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == "__main__":
    import database.models  # Do not alias it
