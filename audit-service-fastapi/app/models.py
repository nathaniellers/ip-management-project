from sqlalchemy import Column, String, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import enum
import uuid
from app.database import Base

class ActionType(str, enum.Enum):
  login = "login"
  logout = "logout"
  create = "create"
  update = "update"
  delete = "delete"

class AuditLog(Base):
  __tablename__ = "audit_logs"

  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  actor_id = Column(UUID(as_uuid=True), nullable=False)
  name = Column(String, nullable=False)
  action = Column(Enum(ActionType), nullable=False)
  ip = Column(String, nullable=False)
  ip_id = Column(UUID(as_uuid=True), nullable=True)
  details = Column(String, default="")
  timestamp = Column(DateTime(timezone=True), server_default=func.now())
