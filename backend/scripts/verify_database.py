
from sqlalchemy import select, func

from app.database import SessionLocal
from app.models import (
    Identity,
    Resource,
    Relationship,
    Vulnerability,
    ActivityLog,
    Simulation,
    Recommendation,
    Approval,
    AgentRun,
    AuditLog,
    WorkflowTest,
    User,
)

models = [
    User,
    Identity,
    Resource,
    Relationship,
    Vulnerability,
    ActivityLog,
    Simulation,
    Recommendation,
    Approval,
    AgentRun,
    AuditLog,
    WorkflowTest,
]

with SessionLocal() as session:
    print("\n========== DATABASE VERIFICATION ==========\n")

    for model in models:
        count = session.scalar(
            select(func.count()).select_from(model)
        )
        print(f"{model.__tablename__}: {count} records")

    payment_bot = session.scalar(
        select(Identity).where(Identity.name == "payment-bot")
    )

    payment_api = session.scalar(
        select(Resource).where(Resource.name == "payment-api")
    )

    customer_db = session.scalar(
        select(Resource).where(Resource.name == "customer-db")
    )

    print("\n========== PAYMENT SCENARIO ==========\n")

    if payment_bot and payment_api and customer_db:
        print("[PASS] payment-bot exists")
        print("[PASS] payment-api exists")
        print("[PASS] customer-db exists")

        payment_edge = session.scalar(
            select(Relationship).where(
                Relationship.source_id == payment_bot.id,
                Relationship.target_id == payment_api.id,
                Relationship.permission == "invoke",
                Relationship.is_active.is_(True),
            )
        )

        database_edge = session.scalar(
            select(Relationship).where(
                Relationship.source_id == payment_api.id,
                Relationship.target_id == customer_db.id,
                Relationship.permission == "read",
                Relationship.is_active.is_(True),
            )
        )

        print(
            "[PASS] payment-bot -> payment-api"
            if payment_edge else
            "[FAIL] payment-bot -> payment-api"
        )

        print(
            "[PASS] payment-api -> customer-db"
            if database_edge else
            "[FAIL] payment-api -> customer-db"
        )
    else:
        print("[FAIL] Required payment scenario records are missing.")

    print("\n=========================================")
