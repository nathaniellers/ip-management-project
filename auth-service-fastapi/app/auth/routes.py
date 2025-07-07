from fastapi import APIRouter, HTTPException, Request, Depends
from typing import Annotated
from sqlalchemy.orm import Session
from app.database.db import get_db
from fastapi.security import OAuth2PasswordRequestForm
from app.auth.models import Token, User, UserLogin, UserCreate
from app.auth.security import oauth2_scheme, get_current_user
from app.auth.services import process_login, process_logout, register_user_to_db, refresh_access_token
from sqlalchemy.orm import Session
import logging
router = APIRouter()

logger = logging.getLogger(__name__)

@router.post("/login", response_model=Token)
async def login_user(request: Request, user_login: UserLogin, db: Session = Depends(get_db)):
	return await process_login(request, user_login.email, user_login.password, "login", db)

@router.post("/logout")
async def logout(request: Request, token: Annotated[str, Depends(oauth2_scheme)]):
	return await process_logout(request, token)

@router.post("/test-protected", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
	return current_user

@router.post("/register", status_code=201)
async def register(request: Request, user: UserCreate, db: Session = Depends(get_db)):
	new_user = await register_user_to_db(request, user, 
																			db)
	return {
		"email": new_user.email,
		"full_name": new_user.full_name,
		"message": "User registered successfully"
	}

@router.post("/token", response_model=Token)
async def login_token(request: Request, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
	return await process_login(request, form_data.username, form_data.password, "token")

@router.post("/refresh")
async def refresh_token_route(request: Request):
	# Step 1: Extract cookie value
	cookie = request.cookies.get("refresh_token")
	
	if not cookie:
		raise HTTPException(status_code=401, detail="Missing refresh token")

	# Step 2: If it's a JSON string or dict, extract the actual token
	refresh_token = None
	if isinstance(cookie, str) and cookie.startswith("{"):
		# If cookie is a stringified JSON, parse it
		import json
		try:
			parsed = json.loads(cookie)
			refresh_token = parsed.get("refresh_token")
		except Exception as e:
			raise HTTPException(status_code=400, detail=f"Malformed refresh_token cookie {e}")
	elif isinstance(cookie, dict):
		refresh_token = cookie.get("refresh_token")
	else:
		# Assume it's a direct token string
		refresh_token = cookie

	if not refresh_token or not isinstance(refresh_token, str):
		raise HTTPException(status_code=401, detail="Invalid refresh token format")

	# Step 3: Call the actual logic
	return await refresh_access_token(refresh_token, request)

