"""Creates sample tenants/plans for local testing."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from auth.api_key import generate, hash_key
from database.base import SessionLocal, engine
from database.base import Base
from database.models.tenant import Tenant


DEMO_TENANTS = [
    ("Acme Corp", "free"),
    ("Globex Corporation", "pro"),
    ("Initech", "enterprise"),
]


def main() -> None:
    """Seed demo tenants with API keys."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        for name, plan in DEMO_TENANTS:
            existing = db.query(Tenant).filter(Tenant.name == name).first()
            if existing:
                print(f"Tenant {name} already exists, skipping.")
                continue
            api_key = generate()
            tenant = Tenant(
                id=name.lower().replace(" ", "_"),
                name=name,
                plan=plan,
                api_key_hash=hash_key(api_key),
            )
            db.add(tenant)
            db.commit()
            print(f"Created tenant '{name}' (plan={plan}) api_key={api_key}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
