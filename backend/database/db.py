from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
import sys
import os
from dotenv import load_dotenv

# 📦 Ensure parent directory is on sys.path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

# 🌱 Load environment variables
load_dotenv()

# 🔗 DB connection (from .env)
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in your .env file")

engine = create_engine(DATABASE_URL)

# 🧠 Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 🧱 User-side model base
Base = declarative_base()

# 📦 Admin-side model base
from database.admin.base import AdminBase  # Separate base for admin tables

# 🛠 Dependency for FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🚀 Reset both user & admin schema (dev only)
if __name__ == "__main__":
    # Import all models to ensure they are registered with their respective bases
    import database.models
    import database.admin.admin_models

    print("⚠️  Dropping and recreating the public schema...")

    with engine.connect() as connection:
        connection.execute(text("DROP SCHEMA public CASCADE;"))
        connection.execute(text("CREATE SCHEMA public;"))
        connection.commit()

    print("✅ Creating all tables from current models...")
    Base.metadata.create_all(bind=engine)
    AdminBase.metadata.create_all(bind=engine)

    print("🎉 Database reset complete.")
