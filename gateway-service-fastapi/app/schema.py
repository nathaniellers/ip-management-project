from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
from datetime import datetime

class LoginRequest(BaseModel):
  email: EmailStr
  password: str

class LogoutRequest(BaseModel):
  token: str

class RegisterRequest(BaseModel):
  email: EmailStr
  password: str
  full_name: str

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

