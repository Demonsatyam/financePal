from sqlalchemy import Column, String, Date, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database.db import Base  # ✅ EDITED: Import from the new core.py
import uuid

# ... (rest of the file remains exactly the same)
class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    email = Column(String, nullable=False)
    dob = Column(String)
    password_hash = Column(String, nullable=False)

    policies = relationship("Policy", back_populates="user")
    claims = relationship("Claim", back_populates="user")


class Policy(Base):
    __tablename__ = "policies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    policy_name = Column(String, nullable=False)
    start_date = Column(Date)
    end_date = Column(Date)
    premium_amount = Column(Integer)
    payment_cycle = Column(String)
    next_due_date = Column(Date)
    status = Column(String)

    user = relationship("User", back_populates="policies")
    clauses = relationship("Clause", back_populates="policy")
    claims = relationship("Claim", back_populates="policy")


class Clause(Base):
    __tablename__ = "clauses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    policy_id = Column(UUID(as_uuid=True), ForeignKey("policies.id"))
    title = Column(String, nullable=False)
    content = Column(String)

    policy = relationship("Policy", back_populates="clauses")


class Claim(Base):
    __tablename__ = "claims"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    policy_id = Column(UUID(as_uuid=True), ForeignKey("policies.id"))
    claim_date = Column(Date)
    claim_type = Column(String)
    amount = Column(Integer)
    status = Column(String)

    user = relationship("User", back_populates="claims")
    policy = relationship("Policy", back_populates="claims")