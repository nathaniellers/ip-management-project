import pytest
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from uuid import uuid4
from app.database import Base
from app.schemas import AuditLogCreate, ActionType, ResourceType
from app.services import create_audit_log_entry, get_filtered_audit_logs
from sqlalchemy.orm import Session
from app.models import AuditLog


SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
  Base.metadata.create_all(bind=engine)
  db = TestingSessionLocal()
  try:
    yield db
  finally:
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_create_and_filter_log(db):
  log_data = AuditLogCreate(
    actor_id=uuid4(),
    session_id="sess-001",
    name="Test User",
    ip="127.0.0.1",
    action=ActionType.login,
    resource=ResourceType.auth,
    details="User login attempt"
  )
  create_audit_log_entry(log_data, db)

  result = get_filtered_audit_logs(
    db=db,
    search="Test",
    action="login",
    resource="auth",
    session_id="sess-001",
    ip="127.0.0.1",
    start_date=datetime.today().strftime("%Y-%m-%d"),
    end_date=(datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d"),
    page=0,
    limit=10
  )

  assert result["total"] == 1
  assert result["logs"][0]["name"] == "Test User"
  assert result["logs"][0]["action"] == "login"
  assert result["logs"][0]["resource"] == "auth"

@pytest.fixture
def seed_logs(db: Session):
  logs = [
    AuditLog(
      id=uuid4(),
      actor_id=uuid4(),
      session_id="sess1",
      name="Alice",
      ip="192.168.0.1",
      action=ActionType.login,
      resource=ResourceType.auth,
      details="Logged in",
      timestamp=datetime.utcnow()
    ),
    AuditLog(
      id=uuid4(),
      actor_id=uuid4(),
      session_id="sess2",
      name="Bob",
      ip="192.168.0.2",
      action=ActionType.delete,
      resource=ResourceType.user,
      details="Deleted a user",
      timestamp=datetime.utcnow()
    ),
  ]
  db.add_all(logs)
  db.commit()
  return logs

def test_invalid_action_raises_exception(db: Session):
  with pytest.raises(HTTPException) as exc_info:
    get_filtered_audit_logs(db, action="invalid")
  assert exc_info.value.status_code == 400
  assert "Invalid action" in str(exc_info.value.detail)

def test_invalid_resource_raises_exception(db: Session):
  with pytest.raises(HTTPException) as exc_info:
    get_filtered_audit_logs(db, resource="invalid")
  assert exc_info.value.status_code == 400
  assert "Invalid resource" in str(exc_info.value.detail)

def test_invalid_start_date_raises_exception(db: Session):
  with pytest.raises(HTTPException) as exc_info:
    get_filtered_audit_logs(db, start_date="bad-date")
  assert exc_info.value.status_code == 400
  assert "Invalid start_date format" in str(exc_info.value.detail)

def test_invalid_end_date_raises_exception(db: Session):
  with pytest.raises(HTTPException) as exc_info:
    get_filtered_audit_logs(db, end_date="not-a-date")
  assert exc_info.value.status_code == 400
  assert "Invalid end_date format" in str(exc_info.value.detail)