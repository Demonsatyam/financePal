from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database.db import get_db  # ✅ EDITED: Import from the new core.py
from database.models import User
import bcrypt
from pydantic import BaseModel, EmailStr

# ... (rest of the file remains exactly the same)
class UserCreate(BaseModel):
    name: str
    phone: str
    email: EmailStr
    dob: str
    password: str


router = APIRouter()

@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    if db.query(User).filter(User.phone == user.phone).first():
        raise HTTPException(status_code=400, detail="Phone already registered")

    # Hash the password
    hashed_pw = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()).decode()

    # Create and store user
    db_user = User(
        name=user.name,
        phone=user.phone,
        email=user.email,
        dob=user.dob,
        password_hash=hashed_pw
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {"msg": "Signup successful", "user_id": str(db_user.id)}


@router.post("/login")
def login(phone: str, password: str, db: Session = Depends(get_db)):
    # Find user by phone number
    user = db.query(User).filter(User.phone == phone).first()

    # Check password
    if not user or not bcrypt.checkpw(password.encode(), user.password_hash.encode()):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"msg": "Login successful", "user_id": str(user.id), "name": user.name}