from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import date
from database.db import get_db
from database.models import User, Policy

router = APIRouter()

@router.post("/link-policy")
def link_policy(
    user_id: UUID = Query(...),
    policy_name: str = Query(...),
    start_date: date = Query(...),
    end_date: date = Query(...),
    premium_amount: int = Query(...),
    payment_cycle: str = Query(...),
    db: Session = Depends(get_db)
):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        policy = Policy(
            user_id=user_id,
            policy_name=policy_name,
            start_date=start_date,
            end_date=end_date,
            premium_amount=premium_amount,
            payment_cycle=payment_cycle,
            status="active",
        )

        db.add(policy)
        db.commit()
        db.refresh(policy)

        return {"msg": "Policy linked", "policy_id": str(policy.id)}

    except Exception as e:
        print("🚨 Exception occurred:", e)
        raise HTTPException(status_code=500, detail=str(e))
