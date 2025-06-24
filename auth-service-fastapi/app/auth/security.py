from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
import uuid

from jose import JWTError, jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.config import settings
from app.auth.models import UserJWT, UserInDB, User
from app.auth.exceptions import AuthException
from app.database.db import get_user_from_db, verify_password
from app.database.redis_db import is_token_blacklisted

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/token")


def create_access_token(
	user_data_for_jwt: UserJWT,
	request_url: str,
	expires_delta: Optional[timedelta] = None
) -> Dict[str, Any]:
	"""
	Creates a new JWT access token with the specified user data.
	Returns the token string and its jti.
	"""
	jti_value = str(uuid.uuid4())
	now = datetime.now(timezone.utc)
	expire = now + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))

	payload: Dict[str, Any] = {
		"sub": str(user_data_for_jwt.email),
		"iss": request_url,
		"iat": now.timestamp(),
		"exp": expire.timestamp(),
		"jti": jti_value,
		"user": {
			**user_data_for_jwt.model_dump(exclude={"id"}),
    	"id": str(user_data_for_jwt.id)
		}

	}

	payload["user"]["id"] = str(user_data_for_jwt.id)

	encoded_jwt = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
	return {
		"access_token": encoded_jwt,
		"jti": jti_value,
		"exp": int(expire.timestamp())
	}


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
	"""
	Dependency to get the current authenticated user from a JWT token.
	Extracts 'user' data from the payload and checks blacklist.
	"""
	try:
		payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

		jti: str = payload.get("jti")
		if jti is None or is_token_blacklisted(jti):
			raise AuthException("Token is invalid or blacklisted")

		user_jwt_data = payload.get("user")
		if not user_jwt_data:
			raise AuthException("User data is missing in token")

		user_jwt = UserJWT(**user_jwt_data)

	except (JWTError, ValueError):
		raise AuthException("Could not validate token")

	user_data_from_db = get_user_from_db(user_jwt.email)
	if user_data_from_db is None:
		raise AuthException("User does not exist")

	user_in_db = UserInDB(**user_data_from_db)
	if user_in_db.disabled:
		raise AuthException("User is inactive", status_code=400)

	return User(
		id=user_in_db.id,
		email=user_in_db.email,
		full_name=user_in_db.full_name,
		disabled=user_in_db.disabled
	)


async def authenticate_user(email: str, password: str) -> Optional[UserInDB]:
	"""
	Authenticates a user against the database.
	"""
	user_data = get_user_from_db(email)
	if not user_data:
		return None

	user = UserInDB(**user_data)
	if not verify_password(password, user.hashed_password):
		return None

	return user

def create_refresh_token(user_data_for_jwt: UserJWT, request_url: str) -> str:
	expire = datetime.now(timezone.utc) + timedelta(days=7)
	jti_value = str(uuid.uuid4())
	payload = {
		"aud": "auth-service",
		"sub": user_data_for_jwt.email,
		"jti": jti_value,
		"scope": "refresh",
		"exp": expire.timestamp(),
		"iat": datetime.now(timezone.utc).timestamp(),
		"user": {
			**user_data_for_jwt.model_dump(exclude={"id"}),
    	"id": str(user_data_for_jwt.id)
		}
	}
	return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
