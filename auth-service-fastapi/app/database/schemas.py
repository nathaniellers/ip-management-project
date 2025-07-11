from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
  email: EmailStr
  password: str
  full_name: str

class UserLogin(BaseModel):
  id: str
  email: EmailStr
  password: str
  full_name: str
  disabled: bool

class LoginRequest(BaseModel):
  email: EmailStr
  password: str

class Token(BaseModel):
  access_token: str
  refresh_token: str
  token_type: str = "bearer"

class RefreshRequest(BaseModel):
  refresh_token: str

