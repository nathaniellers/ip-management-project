from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
  email: EmailStr
  password: str

class LogoutRequest(BaseModel):
  token: str

class RegisterRequest(BaseModel):
  email: EmailStr
  password: str
  full_name: str