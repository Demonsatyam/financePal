# database/seed_data.py
from database.db import Base, engine, SessionLocal
from database.models import User, Policy
from datetime import date

Base.metadata.create_all(bind=engine)
db = SessionLocal()

# Create user
user = User(name="Satyam Kumar", phone="7710291439", email="kumarsatyam01303@gmail.com.com", insurer_id="BAJAJ123")
db.add(user)
db.commit()

# Create policy
policy = Policy(user_id=user.id, insurer="Bajaj Finserv", start_date=date(2025, 4, 1),
                summary="Covers all major surgeries including knee replacement after 60 days.")
db.add(policy)
db.commit()
db.close()
