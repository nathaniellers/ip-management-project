from datetime import timedelta
from fastapi import Request, status, Depends
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from typing import Optional
from app.auth.models import UserJWT, UserCreate
from app.auth.security import authenticate_user, create_access_token, create_refresh_token
from app.auth.exceptions import AuthException
from app.config import settings
from app.database.redis_db import is_token_blacklisted, add_token_to_blacklist
from app.auth.models import RefreshRequest
from app.database.models import User
from app.auth.models import UserCreate, UserInDB
from app.database.crud_user import get_password_hash

async def process_login(request: Request, username: str, password: str, endpoint: str, db: Session):
	user = await authenticate_user(username, password, db)
	if not user:
		raise AuthException(detail="Incorrect credentials")

	user_data = UserJWT(id=user.id, name=user.full_name, email=user.email)
	issuer = f"{request.url.scheme}://{request.url.netloc}/api/{endpoint}"
	access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

	access_token = create_access_token(user_data, issuer, access_token_expires)
	refresh_token = await create_refresh_token(user_data, issuer)

	return {
		"access_token": access_token["access_token"],
		"refresh_token": refresh_token["refresh_token"],
		"token_type": "bearer",
		"expires_in": access_token["exp"],
	}

async def process_logout(token: str):
	try:
		payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
		jti = payload.get("jti")
		exp = payload.get("exp")

		if jti is None or exp is None:
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
		return {"message": "Successfully logged out."}

	except JWTError as e:
		raise AuthException(detail=f"Invalid token for logout. {e}")

async def refresh_access_token(request: Request, body: RefreshRequest):
	try:
		payload = jwt.decode(body.refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

		if payload.get("scope") != "refresh":
			raise AuthException(
				status_code=status.HTTP_403_FORBIDDEN,
				detail="Invalid token scope"
			)

		user_data = payload.get("user")
		if not user_data:
			raise AuthException(
				status_code=status.HTTP_403_FORBIDDEN,
				detail="Missing user info in token"
			)

		user_jwt = UserJWT(**user_data)

		issuer = f"{request.url.scheme}://{request.url.netloc}/api/refresh"
		new_access_token = create_access_token(user_jwt, issuer)

		return {
			"access_token": new_access_token["access_token"],
			"token_type": "bearer"
		}

	except JWTError as e:
		raise AuthException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail=f"Invalid refresh token: {str(e)}"
		)

async def get_user_from_db(db: Session, email: str) -> Optional[User]:
	return db.query(User).filter(User.email == email).first()

async def save_user_to_db(user_data: UserCreate, db: Session) -> User:
	existing = await get_user_from_db(db, user_data.email)

	if existing:
		raise AuthException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="User already exists."
		)

	user = User(
		email=user_data.email,
		# hashed_password=get_password_hash(user_data.password),
		hashed_password=get_password_hash(user_data.password),
		full_name=getattr(user_data, "full_name", None)
	)

	db.add(user)
	db.commit()
	db.refresh(user)
	return user

