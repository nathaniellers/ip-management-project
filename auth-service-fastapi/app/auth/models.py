from typing import Optional
from pydantic import BaseModel, EmailStr, field_serializer
from uuid import UUID

class Token(BaseModel):
	access_token: str
	token_type: str

class TokenData(BaseModel):
	email: Optional[EmailStr] = None

class UserJWT(BaseModel):
	id: UUID
	name: str
	email: EmailStr

	@field_serializer("id")
	def serialize_id(self, value: UUID, _info):
		return str(value)

class User(BaseModel):
	id: UUID
	email: EmailStr
	full_name: Optional[str] = None
	disabled: Optional[bool] = None

class UserInDB(User):
	hashed_password: str

class UserCreate(BaseModel):
	email: EmailStr
	password: str
	full_name: Optional[str] = None

class UserLogin(BaseModel):
	email: EmailStr
	password: str

class TokenWithRefresh(BaseModel):
	access_token: str
	refresh_token: str
	token_type: str = "bearer"

class RefreshRequest(BaseModel):
	refresh_token: str
