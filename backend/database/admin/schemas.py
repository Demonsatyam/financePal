from pydantic import BaseModel
from typing import List, Optional
import uuid

# --- Child Schemas ---
# These define the shape of the nested objects

class BenefitCreate(BaseModel):
    title: str
    description: Optional[str] = None

class ExclusionCreate(BaseModel):
    reason: str

class EligibilityCreate(BaseModel):
    condition: str

class ClauseCreate(BaseModel):
    title: str
    content: Optional[str] = None

# --- Main Policy Schema ---
# This is the main object you will send in your API request.
# It includes lists of the child objects defined above.

class AdminPolicyCreate(BaseModel):
    name: str
    insurer: str
    description: Optional[str] = None
    benefits: List[BenefitCreate] = []
    exclusions: List[ExclusionCreate] = []
    eligibility: List[EligibilityCreate] = []
    clauses: List[ClauseCreate] = []

# --- Response Schema ---
# This defines the shape of the data the API will send back

class AdminPolicyResponse(AdminPolicyCreate):
    id: uuid.UUID

    class Config:
        orm_mode = True # This allows Pydantic to read data from SQLAlchemy objects