from fastapi import APIRouter, Request, Depends
from typing import Annotated
from sqlalchemy.orm import Session
from app.database.db import get_db

from fastapi.security import OAuth2PasswordRequestForm

from app.auth.models import Token, User, UserLogin, UserCreate
from app.auth.security import oauth2_scheme, get_current_user
from app.auth.services import process_login, process_logout, save_user_to_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/login", response_model=Token)
async def login_user(request: Request, user_login: UserLogin, db: Session = Depends(get_db)):
	return await process_login(request, user_login.email, user_login.password, "login", db)

@router.post("/logout")
async def logout(token: Annotated[str, Depends(oauth2_scheme)]):
	return await process_logout(token)

@router.post("/test-protected", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
	return current_user

@router.post("/register", status_code=201)
async def register(user: UserCreate, db: Session = Depends(get_db)):
	new_user = await save_user_to_db(user, db)
	return {
		"email": new_user.email,
		"full_name": new_user.full_name,
		"message": "User registered successfully"
	}