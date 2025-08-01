from sqlalchemy import Column, String, Date, Integer, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base
import uuid

from .base import AdminBase

# --------------------- AdminPolicy Table ---------------------
class AdminPolicy(AdminBase):
    __tablename__ = "admin_policies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(String)
    insurer = Column(String)

    eligibility = relationship("Eligibility", back_populates="policy")
    exclusions = relationship("Exclusion", back_populates="policy")
    benefits = relationship("Benefit", back_populates="policy")
    clauses = relationship("Clause", back_populates="policy")


# --------------------- Eligibility Table ---------------------
class Eligibility(AdminBase):
    __tablename__ = "eligibility"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    policy_id = Column(UUID(as_uuid=True), ForeignKey("admin_policies.id"))
    condition = Column(Text, nullable=False)

    policy = relationship("AdminPolicy", back_populates="eligibility")


# --------------------- Benefit Table ---------------------
class Benefit(AdminBase):
    __tablename__ = "benefits"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    policy_id = Column(UUID(as_uuid=True), ForeignKey("admin_policies.id"))
    title = Column(String, nullable=False)
    description = Column(Text)

    policy = relationship("AdminPolicy", back_populates="benefits")


# --------------------- Exclusion Table ---------------------
class Exclusion(AdminBase):
    __tablename__ = "exclusions"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    policy_id = Column(UUID(as_uuid=True), ForeignKey("admin_policies.id"))
    reason = Column(Text, nullable=False)

    policy = relationship("AdminPolicy", back_populates="exclusions")


# --------------------- Clause Table ---------------------
class Clause(AdminBase):
    # ✅ EDITED: Renamed the table to be unique and avoid conflicts
    __tablename__ = "admin_clauses"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    policy_id = Column(UUID(as_uuid=True), ForeignKey("admin_policies.id"))
    title = Column(String, nullable=False)
    content = Column(Text)

    policy = relationship("AdminPolicy", back_populates="clauses")