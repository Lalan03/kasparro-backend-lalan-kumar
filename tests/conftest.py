#teste/conftest.py

import pytest
from fastapi.testclient import TestClient
from api.main import app
from core.database import SessionLocal, Base, engine


@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app)
