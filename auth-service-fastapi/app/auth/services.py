import logging
from datetime import timedelta
from typing import Optional
from fastapi.responses import JSONResponse
from fastapi import Header, Request, status
from sqlalchemy.orm import Session
from app.auth.models import UserJWT, UserCreate, RefreshRequest
from app.auth.security import authenticate_user, create_access_token, create_refresh_token
from app.auth.exceptions import AuthException
from app.config import settings
from app.database.redis_db import is_token_blacklisted, add_token_to_blacklist
from app.database.models import User
from app.database.crud_user import get_password_hash
from app.queue.audit_queue import enqueue_audit_log
from app.auth.utils.token import decode_token
from app.auth.utils.ip import get_client_ip
import shortuuid

logger = logging.getLogger(__name__)

async def process_login(request: Request, username: str, password: str, endpoint: str, db: Session):
	
	user = await authenticate_user(username, password, db)
	if not user:
		logger.warning(f"Failed login attempt for: {username}")
		raise AuthException(detail="Incorrect credentials")

	session_id = f"sess_{shortuuid.uuid()}"
	
	user_data = UserJWT(
		id=user.id,
		name=user.full_name,
		email=user.email,
		role=user.role,
		session_id=session_id
	)

	issuer = f"{request.url.scheme}://{request.url.netloc}/api/{endpoint}"
	access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
	token = create_access_token(user_data, issuer, access_token_expires)
	refresh_token = await create_refresh_token(user_data, issuer)

	ip = get_client_ip(request)

	await enqueue_audit_log({
		"actor_id": str(user.id),
		"name": user.full_name,
		"action": "login",
		"resource": "auth",
		"ip": ip,
		"session_id": session_id,
		"details": "User logged in"
	})

	response = JSONResponse(
		content={"access_token": token['access_token']},
		status_code=200
	)
	
	response.set_cookie(
		key="refresh_token",
		value=refresh_token['refresh_token'],
		httponly=True,
		samesite="Lax",
		secure=False
	)

	return response

async def process_logout(request: Request, token: str):
	payload = decode_token(token)
	jti = payload.get("jti")
	exp = payload.get("exp")

	if not jti or not exp:
		raise AuthException(
			detail="Invalid token for logout: Missing JTI or expiration.",
			status_code=status.HTTP_400_BAD_REQUEST
		)

	if is_token_blacklisted(jti):
		raise AuthException(
			detail="Token already blacklisted.",
			status_code=status.HTTP_400_BAD_REQUEST
		)

	add_token_to_blacklist(jti, exp)
	
	ip = get_client_ip(request)

	await enqueue_audit_log({
		"actor_id": str(payload.get("user", {}).get("id", "")),
		"name": payload.get("user", {}).get("name", ""),
		"action": "logout",
    "resource": "auth",
		"ip": ip,
		"details": "User logged out",
    "session_id": str(payload.get("user", {}).get("session_id", "")),
	})

	return {"message": "Successfully logged out."}

async def refresh_access_token(refresh_token: str, request: Request):
	payload = decode_token(refresh_token, expected_scope="refresh")
	user_data = payload.get("user")
	if not user_data:
			raise AuthException(status_code=403, detail="Missing user info in token")

	user_jwt = UserJWT(**user_data)
	issuer = f"{request.url.scheme}://{request.url.netloc}/api/refresh"
	new_access_token = create_access_token(user_jwt, issuer)
	new_refresh_token = await create_refresh_token(user_jwt, issuer)

	return {
			"access_token": new_access_token["access_token"],
			"token_type": "bearer",
			"refresh_token": new_refresh_token['refresh_token']
	}

async def get_user_from_db(db: Session, email: str) -> Optional[User]:
	logger.debug(f"Fetching user from DB: {email}")
	return db.query(User).filter(User.email == email).first()

async def save_user_to_db(
	user_data: UserCreate,
	db: Session,
	authorization: str = Header(...)
) -> User:

	existing = await get_user_from_db(db, user_data.email)
	if existing:
		logger.warning(f"User already exists: {user_data.email}")
		raise AuthException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="User already exists."
		)

	token = authorization.replace("Bearer ", "")
	payload = decode_token(token)
	session_id = payload.get("user", {}).get("session_id")

	user = User(
		email=user_data.email,
		hashed_password=get_password_hash(user_data.password),
		full_name=getattr(user_data, "full_name", None)
	)

	db.add(user)
	db.commit()
	db.refresh(user)

	await enqueue_audit_log({
		"actor_id": str(user.id),
		"name": user.full_name,
		"action": "register",
		"resource": "auth",
		"session_id": session_id or "",
		"details": f"User {user.email} registered"
	})

	return user

async def register_user_to_db(
		request,
    user_data: UserCreate,
    db: Session,
    authorization: str = None
) -> User:

	existing = await get_user_from_db(db, user_data.email)
	if existing:
		logger.warning(f"User already exists: {user_data.email}")
		raise AuthException(
			status_code=400,
			detail="User already exists."
		)

	session_id = None
	if authorization:
		token = authorization.replace("Bearer ", "")
		session_id = decode_token(token)

	user = User(
		email=user_data.email,
		hashed_password=get_password_hash(user_data.password),
		full_name=getattr(user_data, "full_name", None),
	)

	db.add(user)
	db.commit()
	db.refresh(user)

	ip = get_client_ip(request)

	await enqueue_audit_log({
		"actor_id": str(user.id),
		"name": user.full_name,
		"action": "register",
		"resource": "auth",
		"ip": ip,
		"session_id": session_id or "",
		"details": f"User {user.email} registered"
	})

	return user