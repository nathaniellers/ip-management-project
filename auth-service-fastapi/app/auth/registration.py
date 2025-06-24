from fastapi import HTTPException, status
from app.auth.models import UserCreate, UserInDB
from app.database.db import get_user_from_db, save_user_to_db, get_password_hash


def register_user(user_data: UserCreate) -> UserInDB:
	existing = get_user_from_db(user_data.email)
	if existing:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="User already exists."
		)

	hashed_pw = get_password_hash(user_data.password)
	new_user = {
		"email": user_data.email,
		"full_name": user_data.full_name,
		"hashed_password": hashed_pw,
		"disabled": False
	}

	save_user_to_db(new_user)
	return UserInDB(**new_user)
