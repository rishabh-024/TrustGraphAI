import json
from pathlib import Path

from sqlalchemy.orm import Session

from app.database import Base, engine
from app.models import (
    Identity,
    Resource,
    Relationship,
    Vulnerability,
    ActivityLog,
)

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

DATASETS = [
    ("identities.json", Identity),
    ("resources.json", Resource),
    ("relationships.json", Relationship),
    ("vulnerabilities.json", Vulnerability),
    ("activity_logs.json", ActivityLog),
]


def load_records(filename):
    path = DATA_DIR / filename

    if not path.exists():
        raise FileNotFoundError(f"Missing dataset: {path}")

    try:
        with path.open("r", encoding="utf-8") as file:
            records = json.load(file)
    except json.JSONDecodeError as error:
        raise ValueError(f"Malformed JSON in {filename}: {error}") from error

    if not isinstance(records, list):
        raise ValueError(f"{filename} must contain a JSON list.")

    seen_ids = set()

    for index, record in enumerate(records):
        if not isinstance(record, dict):
            raise ValueError(
                f"{filename}: record {index} must be a JSON object."
            )

        record_id = record.get("id")

        if not record_id:
            raise ValueError(
                f"{filename}: record {index} has no ID."
            )

        if record_id in seen_ids:
            raise ValueError(
                f"{filename}: duplicate ID found: {record_id}"
            )

        if record.get("is_synthetic") is not True:
            raise ValueError(
                f"{filename}: {record_id} is not marked synthetic."
            )

        seen_ids.add(record_id)

    return records


def seed_database():
    Base.metadata.create_all(bind=engine)

    with Session(engine) as session:
        try:
            for filename, model in DATASETS:
                records = load_records(filename)
                inserted = 0
                updated = 0

                for record in records:
                    existing = session.get(model, record["id"])

                    if existing:
                        updated += 1
                    else:
                        inserted += 1

                    # Insert new records or update existing records.
                    session.merge(model(**record))

                print(
                    f"{filename}: "
                    f"{inserted} new, {updated} existing"
                )

            session.commit()
            print("\nDatabase seeding completed successfully.")

        except Exception:
            session.rollback()
            raise


if __name__ == "__main__":
    seed_database()
