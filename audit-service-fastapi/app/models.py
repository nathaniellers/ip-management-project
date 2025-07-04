from sqlalchemy import Column, String, DateTime, Enum as SqlEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy import Enum as SQLAlchemyEnum
from app.schemas import ResourceType

import enum
from uuid import uuid4
from app.database import Base

class ActionType(str, enum.Enum):
  login = "login"
  logout = "logout"
  create = "create"
  update = "update"
  delete = "delete"

class AuditLog(Base):
  __tablename__ = "audit_logs"

  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
  actor_id = Column(UUID(as_uuid=True), nullable=False)
  session_id = Column(String, nullable=True)
  name = Column(String, nullable=False)
  action = Column(SQLAlchemyEnum(ActionType), nullable=False)
  resource = Column(SQLAlchemyEnum(ResourceType), nullable=False)
  ip = Column(String, nullable=True)
  ip_id = Column(UUID(as_uuid=True), nullable=True)
  details = Column(String, default="")
  timestamp = Column(DateTime(timezone=True), server_default=func.now())
