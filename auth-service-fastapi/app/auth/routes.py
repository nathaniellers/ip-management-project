from fastapi import APIRouter, Request, Depends
from typing import Annotated

from fastapi.security import OAuth2PasswordRequestForm

from app.auth.models import Token, User, UserLogin, UserCreate
from app.auth.security import oauth2_scheme, get_current_user
from app.auth.services import process_login, process_logout
from app.auth.registration import register_user

router = APIRouter(
	prefix="/api",
	tags=["Authentication"],
)

@router.post("/token", response_model=Token)
async def login_token(request: Request, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
	token = await process_login(request, form_data.username, form_data.password, "token")
	return {"access_token": token["access_token"], "token_type": "bearer"}

@router.post("/login", response_model=Token)
async def login_user(request: Request, user_login: UserLogin):
	token = await process_login(request, user_login.email, user_login.password, "login")
	return {"access_token": token["access_token"], "token_type": "bearer"}

@router.post("/logout")
async def logout(token: Annotated[str, Depends(oauth2_scheme)]):
	return await process_logout(token)

@router.post("/test-protected", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
	return current_user

@router.post("/register", status_code=201)
async def register(user: UserCreate):
	new_user = await register_user(user)
	return {"email": new_user.email, "message": "User registered successfully"}
