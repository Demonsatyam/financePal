from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.db import SessionLocal
from database.models import User

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login")
def login(phone: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.phone == phone).first()
    if user:
        return {"user_id": str(user.id), "name": user.name}
    return {"error": "User not found"}
