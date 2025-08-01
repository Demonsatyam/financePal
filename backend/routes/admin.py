from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

# Import our new schemas and the necessary database components
from database.admin.schemas import AdminPolicyCreate, AdminPolicyResponse
from database.admin import admin_models
from database.db import get_db

router = APIRouter()

@router.post(
    "/policies", 
    response_model=AdminPolicyResponse,
    summary="Create a new Admin Policy",
    description="Creates a new administrative policy along with all its associated benefits, exclusions, eligibility criteria, and clauses."
)
def create_admin_policy(policy_data: AdminPolicyCreate, db: Session = Depends(get_db)):
    """
    Endpoint to create a new AdminPolicy and all its related child objects.
    """
    # Check if a policy with this name already exists
    existing_policy = db.query(admin_models.AdminPolicy).filter(admin_models.AdminPolicy.name == policy_data.name).first()
    if existing_policy:
        raise HTTPException(
            status_code=400,
            detail=f"Policy with name '{policy_data.name}' already exists."
        )

    try:
        # 1. Create the main AdminPolicy object
        db_policy = admin_models.AdminPolicy(
            name=policy_data.name,
            insurer=policy_data.insurer,
            description=policy_data.description
        )

        # 2. Create and associate all the child objects
        # SQLAlchemy's relationships are smart enough to handle the linking.
        
        for benefit_data in policy_data.benefits:
            db_policy.benefits.append(admin_models.Benefit(**benefit_data.dict()))

        for exclusion_data in policy_data.exclusions:
            db_policy.exclusions.append(admin_models.Exclusion(**exclusion_data.dict()))
            
        for eligibility_data in policy_data.eligibility:
            db_policy.eligibility.append(admin_models.Eligibility(**eligibility_data.dict()))

        for clause_data in policy_data.clauses:
            db_policy.clauses.append(admin_models.Clause(**clause_data.dict()))

        # 3. Add to the session and commit to the database
        # This will save the parent policy and all the child objects in one transaction.
        db.add(db_policy)
        db.commit()

        # 4. Refresh the object to get the new ID and other DB-generated values
        db.refresh(db_policy)

        return db_policy

    except Exception as e:
        db.rollback() # Rollback the transaction in case of an error
        print(f"🚨 An error occurred: {e}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while creating the policy."
        )