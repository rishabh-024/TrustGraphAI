
import json
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

random.seed(42)

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------
# 1. NON-HUMAN IDENTITIES
# -------------------------------------------------

identity_names = [
    "payment-bot", "backup-agent", "reporting-agent", "cloud-api",
    "billing-service", "notification-bot", "data-pipeline",
    "analytics-agent", "inventory-service", "auth-service",
    "deployment-bot", "monitoring-agent", "customer-support-bot",
    "fraud-detection-agent", "email-service", "hr-integration",
    "devops-agent", "security-scanner", "logging-service",
    "document-processor", "ai-assistant-agent", "scheduler-service",
    "warehouse-bot", "audit-agent", "database-maintenance"
]

identity_types = ["service_account", "api_identity", "machine_identity", "ai_agent"]

identities = []
for index, name in enumerate(identity_names, start=1):
    identities.append({
        "id": f"ID-{index:03}",
        "name": name,
        "identity_type": identity_types[(index - 1) % len(identity_types)],
        "environment": random.choice(["production", "staging", "development"]),
        "owner": random.choice(["Payments", "Platform", "Security", "Data", "HR"]),
        "status": "active",
        "created_at": "2026-01-15T10:00:00Z",
        "is_synthetic": True
    })

# -------------------------------------------------
# 2. ENTERPRISE RESOURCES
# -------------------------------------------------

resource_names = [
    "payment-api", "customer-db", "HR-db", "admin-api", "dev-cluster",
    "billing-api", "notification-api", "reporting-db", "auth-api",
    "identity-service", "production-cluster", "staging-cluster",
    "analytics-db", "object-storage", "backup-storage",
    "logging-api", "monitoring-dashboard", "fraud-api",
    "inventory-db", "email-gateway", "secrets-vault",
    " CI-runner", "deployment-api", "audit-db",
    "employee-portal", "document-api", "AI-inference-api",
    "model-registry", "data-warehouse", "message-queue",
    "customer-portal", "metrics-db", "config-service",
    "security-dashboard", "file-storage"
]

resource_types = [
    "api", "database", "cloud_resource", "application",
    "cluster", "storage", "security_service"
]

resources = []
for index, name in enumerate(resource_names, start=1):
    critical = name in {
        "payment-api", "customer-db", "HR-db", "admin-api",
        "production-cluster", "secrets-vault", "billing-api"
    }

    resources.append({
        "id": f"RES-{index:03}",
        "name": name.strip(),
        "resource_type": resource_types[(index - 1) % len(resource_types)],
        "environment": "production" if critical else random.choice(
            ["production", "staging", "development"]
        ),
        "criticality": "critical" if critical else random.choice(
            ["low", "medium", "high"]
        ),
        "business_owner": random.choice(["Payments", "Platform", "Security", "Data"]),
        "is_synthetic": True
    })

identity_ids = [item["id"] for item in identities]
resource_ids = [item["id"] for item in resources]
resource_by_name = {item["name"]: item["id"] for item in resources}

# -------------------------------------------------
# 3. ACCESS AND RESOURCE RELATIONSHIPS
# -------------------------------------------------

relationships = []
used_pairs = set()

def add_relationship(source_id, source_type, target_id, target_type,
                     permission, is_active=True, last_used_days=5):
    pair = (source_id, target_id)

    if pair in used_pairs:
        return

    used_pairs.add(pair)
    last_used = datetime.now(timezone.utc) - timedelta(days=last_used_days)

    relationships.append({
        "id": f"REL-{len(relationships) + 1:03}",
        "source_id": source_id,
        "source_type": source_type,
        "target_id": target_id,
        "target_type": target_type,
        "permission": permission,
        "relationship_type": "access",
        "is_active": is_active,
        "last_used_at": last_used.isoformat(),
        "evidence": "synthetic_access_record",
        "is_synthetic": True
    })

# Core payment workflow and excessive permissions.
payment_bot = identities[0]["id"]

add_relationship(payment_bot, "identity", resource_by_name["payment-api"],
                 "resource", "invoke", True, 1)

add_relationship(resource_by_name["payment-api"], "resource",
                 resource_by_name["customer-db"], "resource", "read", True, 1)

add_relationship(payment_bot, "identity", resource_by_name["HR-db"],
                 "resource", "read", True, 120)

add_relationship(payment_bot, "identity", resource_by_name["admin-api"],
                 "resource", "admin", True, 180)

add_relationship(payment_bot, "identity", resource_by_name["dev-cluster"],
                 "resource", "execute", True, 150)

# Generate additional identity-to-resource access.
permissions_list = ["read", "write", "execute", "invoke", "admin"]

while len(relationships) < 75:
    identity_id = random.choice(identity_ids)
    resource_id = random.choice(resource_ids)

    add_relationship(
        identity_id, "identity", resource_id, "resource",
        random.choice(permissions_list),
        random.choice([True, True, True, False]),
        random.randint(1, 200)
    )

# Generate resource-to-resource relationships.
while len(relationships) < 100:
    source_id, target_id = random.sample(resource_ids, 2)

    add_relationship(
        source_id, "resource", target_id, "resource",
        random.choice(["read", "invoke", "connect"]),
        random.choice([True, True, True, False]),
        random.randint(1, 200)
    )

# -------------------------------------------------
# 4. VULNERABILITIES
# -------------------------------------------------

vulnerabilities = []

severity_levels = ["critical", "high", "medium", "low"]

for index in range(12):
    affected_resource = resources[index]["id"]

    vulnerabilities.append({
        "id": f"VULN-{index + 1:03}",
        "cve_id": f"CVE-2026-{1000 + index}",
        "affected_resource_id": affected_resource,
        "severity": severity_levels[index % len(severity_levels)],
        "description": f"Synthetic security finding for {resources[index]['name']}",
        "status": random.choice(["open", "under_review"]),
        "is_synthetic": True
    })

# Ensure the payment API has a critical vulnerability.
vulnerabilities[0]["affected_resource_id"] = resource_by_name["payment-api"]
vulnerabilities[0]["severity"] = "critical"
vulnerabilities[0]["description"] = (
    "Synthetic critical vulnerability affecting the payment API"
)


# -------------------------------------------------
# 5. ACTIVITY LOGS
# -------------------------------------------------

activity_logs = []
actions = ["read", "write", "execute", "invoke", "admin"]

identity_access = [
    relationship for relationship in relationships
    if relationship["source_type"] == "identity"
    and relationship["target_type"] == "resource"
]

for index in range(300):
    relationship = random.choice(identity_access)

    activity_logs.append({
        "id": f"ACT-{index + 1:04}",
        "identity_id": relationship["source_id"],
        "resource_id": relationship["target_id"],
        "action": relationship["permission"],
        "timestamp": (
            datetime.now(timezone.utc) -
            timedelta(hours=random.randint(1, 1500))
        ).isoformat(),
        "result": random.choice(["success", "success", "success", "denied"]),
        "source": "synthetic_activity_generator",
        "is_synthetic": True
    })

# -------------------------------------------------
# 6. PERMISSIONS (DERIVED FROM IDENTITY ACCESS)
# -------------------------------------------------

permissions = [
    {
        "id": f"PERM-{index + 1:03}",
        "relationship_id": relationship["id"],
        "identity_id": relationship["source_id"],
        "resource_id": relationship["target_id"],
        "permission": relationship["permission"],
        "is_active": relationship["is_active"],
        "is_synthetic": True
    }
    for index, relationship in enumerate(relationships)
    if relationship["source_type"] == "identity"
    and relationship["target_type"] == "resource"
]

# -------------------------------------------------
# 7. SAVE JSON FILES
# -------------------------------------------------

datasets = {
    "identities.json": identities,
    "resources.json": resources,
    "relationships.json": relationships,
    "vulnerabilities.json": vulnerabilities,
    "activity_logs.json": activity_logs,
    "permissions.json": permissions
}

for filename, records in datasets.items():
    output_path = DATA_DIR / filename

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(records, file, indent=4)

    print(f"Created {filename}: {len(records)} records")

print("\nSynthetic dataset generation completed.")
print(f"Output directory: {DATA_DIR}")
