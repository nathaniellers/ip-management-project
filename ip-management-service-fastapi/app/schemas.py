from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime
from app.models import ActionType

class IPCreate(BaseModel):
	ip: str
	label: str
	comment: Optional[str] = None

class IPUpdate(BaseModel):
	label: str
	comment: Optional[str] = None

class IPOut(BaseModel):
  id: UUID
  ip: str
  label: str
  comment: Optional[str]
  created_by: UUID
  updated_at: datetime

  class Config:
    from_attributes = True
