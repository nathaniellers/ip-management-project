import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database.models import Base
from app.database.db import get_db

TEST_DATABASE_URL = "postgresql://postgres:password@localhost:5432/test_db"

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
	db = TestingSessionLocal()
	try:
		yield db
	finally:
		db.close()

app.dependency_overrides[get_db] = override_get_db

Base.metadata.create_all(bind=engine)

@pytest.fixture
def client():
	return TestClient(app)
