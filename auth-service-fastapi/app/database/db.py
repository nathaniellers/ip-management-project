import uuid
from typing import Dict, Any
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

USERS_DB: Dict[str, Dict[str, Any]] = {
	"john.doe@example.com": {
		"id": str(uuid.uuid4()),
		"email": "john.doe@example.com",
		"hashed_password": pwd_context.hash("securepassword123"),
		"full_name": "John Doe",
		"disabled": False,
	},
	"jane.smith@example.com": {
		"id": str(uuid.uuid4()),
		"email": "jane.smith@example.com",
		"hashed_password": pwd_context.hash("anothersecurepass"),
		"full_name": "Jane Smith",
		"disabled": True,
	},
	"nathanielleromero18@gmail.com": {
		"id": str(uuid.uuid4()),
		"email": "nathanielleromero18@gmail.com",
		"hashed_password": pwd_context.hash("mysecretpass"),
		"full_name": "Nathan Romero",
		"disabled": False,
	}
}

def save_user_to_db(user_data: Dict[str, Any]):
	"""
	Adds a new user to the in-memory USERS_DB.
	"""
	USERS_DB[user_data["email"]] = {
		"id": str(uuid.uuid4()), 
		"email": user_data["email"],
		"hashed_password": user_data["hashed_password"],
		"full_name": user_data.get("full_name", ""),
		"disabled": user_data.get("disabled", False)
	}


def get_user_from_db(email: str):
	return USERS_DB.get(email)

def verify_password(plain_password: str, hashed_password: str) -> bool:
	return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
	return pwd_context.hash(password)