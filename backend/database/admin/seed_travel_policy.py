from sqlalchemy.orm import Session
from database.db import SessionLocal
from database.admin.admin_models import AdminPolicy, Eligibility, Benefit, Exclusion, Clause
import uuid

def seed_travel_policy():
    db: Session = SessionLocal()

    existing = db.query(AdminPolicy).filter_by(name="Travel Insurance").first()
    if existing:
        print("⚠️ Travel Insurance policy already exists.")
        db.close()
        return

    policy = AdminPolicy(
        id=uuid.uuid4(),
        name="Travel Insurance",
        insurer="Cholamandalam MS General Insurance",
        description="Covers domestic travel emergencies like accidents, hospitalization, and air ambulance support."
    )
    db.add(policy)
    db.commit()
    db.refresh(policy)

    criteria = [
        "Age between 3 months and 90 years",
        "Must be an Indian resident",
        "Must be part of a registered group policy"
    ]
    # ✅ EDITED: Changed 'criterion=c' to 'condition=c' to match the model
    db.add_all([Eligibility(policy_id=policy.id, condition=c) for c in criteria])

    benefits = [
        ("Emergency Accidental Hospitalization", "Covers inpatient care, diagnostics, and a 7-day extension if unfit to return."),
        ("OPD Treatment (Accidents)", "Covers outpatient care for accident-related injuries."),
        ("Personal Accident Cover", "100% payout for accidental death or permanent disability.")
    ]
    db.add_all([Benefit(policy_id=policy.id, title=title, description=desc) for title, desc in benefits])

    exclusions = [
        "Pre-existing conditions (except life-threatening)",
        "Pregnancy, childbirth, infertility treatment",
        "Cosmetic procedures and experimental treatment",
        "Adventure sports, war, or self-inflicted injuries"
    ]
    # ✅ EDITED: There was likely a similar error here. The model's column is 'reason'.
    db.add_all([Exclusion(policy_id=policy.id, reason=e) for e in exclusions])

    clauses = [
        Clause(
            policy_id=policy.id,
            title="Hospitalization Clause",
            content="Only accidents during travel are covered. Non-accidental illness is not covered unless life-threatening."
        ),
        Clause(
            policy_id=policy.id,
            title="Air Ambulance Clause",
            content="Air ambulance is reimbursed only in life-threatening emergencies when road transport is unavailable."
        )
    ]
    db.add_all(clauses)

    db.commit()
    db.close()
    print("✅ Travel Insurance policy seeded successfully.")

if __name__ == "__main__":
    seed_travel_policy()