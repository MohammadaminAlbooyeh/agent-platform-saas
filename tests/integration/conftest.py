import os
import tempfile

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.models.document import Base
from backend.models.database import get_db
from backend.main import app


@pytest.fixture(scope="session", autouse=True)
def test_db():
    with tempfile.NamedTemporaryFile(suffix=".db") as f:
        os.environ["DATABASE_URL"] = f"sqlite:///{f.name}"
        engine = create_engine(f"sqlite:///{f.name}", connect_args={"check_same_thread": False})
        Base.metadata.create_all(bind=engine)
        TestSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

        def override_get_db():
            db = TestSession()
            try:
                yield db
            finally:
                db.close()

        app.dependency_overrides[get_db] = override_get_db

        yield

        app.dependency_overrides.clear()
        Base.metadata.drop_all(bind=engine)
