# database/models.py
from sqlalchemy import Column, String, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from database.db import Base
import uuid

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    phone = Column(String, unique=True)
    email = Column(String)
    insurer_id = Column(String)

class Policy(Base):
    __tablename__ = "policies"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    insurer = Column(String)
    start_date = Column(Date)
    summary = Column(String)
