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
  ip: str
  ip_id: Optional[UUID] = None
  details: Optional[str] = ""

class AuditLogOut(AuditLogCreate):
  timestamp: datetime

# class AuditLogOut(BaseModel):
# 	id: UUID
# 	actor_id: UUID
# 	name: str
# 	ip: str
# 	ip_id: Optional[UUID]
# 	action: ActionType
# 	timestamp: datetime
# 	details: Optional[str]

# 	class Config:
# 		from_attributes = True