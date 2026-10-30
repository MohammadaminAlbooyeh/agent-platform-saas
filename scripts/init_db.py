"""DB bootstrap: initialize the database schema."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

# Import all models so they register on Base.metadata before create_all.
from database.base import init_db, Base  # noqa: F401
from database.models import tenant, usage_record, invoice, task  # noqa: F401


def main() -> None:
    """Create all tables defined on the Base metadata."""
    init_db()
    print("Database initialized.")


if __name__ == "__main__":
    main()
