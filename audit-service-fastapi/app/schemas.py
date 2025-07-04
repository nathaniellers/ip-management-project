from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from enum import Enum
from typing import Optional

class ActionType(str, Enum):
  login = "login"
  logout = "logout"
  create = "create"
  update = "update"
  delete = "delete"

class AuditLogCreate(BaseModel):
  actor_id: UUID
  name: str
  action: ActionType
  ip: Optional[str] = None
  ip_id: Optional[UUID] = None
  session_id: Optional[str]
  details: Optional[str] = ""
  resource: Optional[str] = ""
  timestamp: Optional[datetime] = None

class AuditLogOut(BaseModel):
	id: UUID
	actor_id: UUID
	session_id: Optional[str]
	name: str
	ip: Optional[str]
	ip_id: Optional[UUID]
	action: ActionType
	timestamp: datetime
	details: Optional[str]
	resource: Optional[str]

	class Config:
		from_attributes = True

class ResourceType(str, Enum):
    auth = "auth"
    ip = "ip"
    user = "user"
