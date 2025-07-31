from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.db import SessionLocal
from database.models import Policy

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/policy/{user_id}")
def get_policy(user_id: str, db: Session = Depends(get_db)):
    policy = db.query(Policy).filter(Policy.user_id == user_id).first()
    if policy:
        return {
            "summary": policy.summary,
            "start_date": policy.start_date.isoformat(),
            "insurer": policy.insurer
        }
    return {"error": "Policy not found"}
