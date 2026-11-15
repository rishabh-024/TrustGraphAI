import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

def load_json(filename):
    path = DATA_DIR / filename
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)

identities = load_json("identities.json")
resources = load_json("resources.json")
relationships = load_json("relationships.json")
vulnerabilities = load_json("vulnerabilities.json")

identity_by_name = {item["name"]: item for item in identities}
resource_by_name = {item["name"]: item for item in resources}

payment_bot = identity_by_name.get("payment-bot")
payment_api = resource_by_name.get("payment-api")
customer_db = resource_by_name.get("customer-db")
hr_db = resource_by_name.get("HR-db")
admin_api = resource_by_name.get("admin-api")
dev_cluster = resource_by_name.get("dev-cluster")

def has_relationship(source_id, target_id, permission):
    return any(
        edge["source_id"] == source_id
        and edge["target_id"] == target_id
        and edge["permission"] == permission
        and edge["is_active"] is True
        for edge in relationships
    )

checks = {
    "payment-bot can invoke payment-api": (
        payment_bot and payment_api and
        has_relationship(payment_bot["id"], payment_api["id"], "invoke")
    ),
    "payment-api can read customer-db": (
        payment_api and customer_db and
        has_relationship(payment_api["id"], customer_db["id"], "read")
    ),
    "payment-bot has access to HR-db": (
        payment_bot and hr_db and
        has_relationship(payment_bot["id"], hr_db["id"], "read")
    ),
    "payment-bot has admin access to admin-api": (
        payment_bot and admin_api and
        has_relationship(payment_bot["id"], admin_api["id"], "admin")
    ),
    "payment-bot can execute dev-cluster": (
        payment_bot and dev_cluster and
        has_relationship(payment_bot["id"], dev_cluster["id"], "execute")
    ),
    "payment-api has a critical vulnerability": (
        payment_api and any(
            item["affected_resource_id"] == payment_api["id"]
            and item["severity"] == "critical"
            for item in vulnerabilities
        )
    )
}

print("\n========== PAYMENT-BOT SCENARIO VERIFICATION ==========\n")

for description, passed in checks.items():
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {description}")

print("\n=======================================================")

if all(checks.values()):
    print("SUCCESS: All payment-bot scenario checks passed.")
else:
    print("WARNING: Some checks failed. Review the generated dataset.")
