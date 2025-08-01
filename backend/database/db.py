from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
import sys
import os

# ... (the top part of your file remains the same) ...

# 📦 Ensure parent directory is on sys.path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

# 🔗 DB connection
DATABASE_URL = "postgresql://postgres:8762@localhost:5432/insurance_db"
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

    # ✅ EDITED: Use raw SQL with CASCADE for a foolproof reset.
    # This directly tells PostgreSQL to drop all tables, views, etc.
    # in the public schema, ignoring dependency order.
    with engine.connect() as connection:
        connection.execute(text("DROP SCHEMA public CASCADE;"))
        connection.execute(text("CREATE SCHEMA public;"))
        connection.commit() # Make sure the changes are committed

    print("✅ Creating all tables from current models...")
    # Now that the database is empty, create_all will succeed.
    Base.metadata.create_all(bind=engine)
    AdminBase.metadata.create_all(bind=engine)

    print("🎉 Database reset complete.")