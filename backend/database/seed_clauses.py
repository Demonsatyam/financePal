from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date
import uuid

from database.models import Clause, Policy
from database.db import Base

# 🔐 Use your actual DB credentials
DATABASE_URL = "postgresql://postgres:8762@localhost:5432/insurance_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)

def seed_clauses():
    db: Session = SessionLocal()

    # 🔍 Find existing policy by name
    policy = db.query(Policy).filter_by(policy_name="Easy Health").first()

    if not policy:
        print("❌ No policy named 'Easy Health' found. Please add one via API first.")
        db.close()
        return

    # ✅ Attach clauses to that real policy
    clauses = [
        Clause(
            id=uuid.uuid4(),
            policy_id=policy.id,
            title="Knee Surgery Coverage",
            content="Covers knee replacement surgeries after a 60-day waiting period."
        ),
        Clause(
            id=uuid.uuid4(),
            policy_id=policy.id,
            title="Baby Care Clause",
            content="Provides coverage for postnatal care and newborn medical expenses up to 6 months."
        ),
        Clause(
            id=uuid.uuid4(),
            policy_id=policy.id,
            title="Ambulance Coverage",
            content="Covers ambulance charges up to ₹2500 per hospitalization event."
        )
    ]

    db.add_all(clauses)
    db.commit()
    db.close()
    print("✅ Clauses linked to 'Easy Health' policy and inserted successfully.")

if __name__ == "__main__":
    seed_clauses()
