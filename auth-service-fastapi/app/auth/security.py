from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
import uuid

from jose import JWTError, jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.config import settings
from app.auth.models import UserJWT, User
from app.auth.exceptions import AuthException
from app.database.crud_user import get_user_by_email, verify_password
from app.database.db import get_db
from app.database.redis_db import is_token_blacklisted

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/token")


def create_access_token(user_data_for_jwt: UserJWT, request_url: str, expires_delta: Optional[timedelta] = None) -> Dict[str, Any]:
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
            "id": str(user_data_for_jwt.id),
            "role": str(user_data_for_jwt.role)
        }
    }

    encoded_jwt = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return {
        "access_token": encoded_jwt,
        "jti": jti_value,
        "exp": int(expire.timestamp())
    }


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
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

    user_obj = get_user_by_email(db, user_jwt.email)
    if user_obj is None:
        raise AuthException("User does not exist")

    if user_obj.disabled:
        raise AuthException("User is inactive", status_code=400)

    return {
        "id": user_obj.id,
        "email": user_obj.email,
        "full_name": user_obj.full_name,
        "disabled": user_obj.disabled,
        "role": user_obj.role
    }


async def authenticate_user(email: str, password: str, db: Session) -> Optional[User]:
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


async def create_refresh_token(user_data_for_jwt: UserJWT, request_url: str, expires_delta: Optional[timedelta] = None) -> Dict[str, Any]:
    jti_value = str(uuid.uuid4())
    now = datetime.now(timezone.utc)
    expire = now + (expires_delta or timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS))

    payload: Dict[str, Any] = {
        "sub": str(user_data_for_jwt.email),
        "iss": request_url,
        "iat": now.timestamp(),
        "exp": expire.timestamp(),
        "jti": jti_value,
        "token_type": "refresh",
        "user": {
            **user_data_for_jwt.model_dump(exclude={"id"}),
            "id": str(user_data_for_jwt.id),
            "role": str(user_data_for_jwt.role)
        }
    }

    encoded_jwt = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return {
        "refresh_token": encoded_jwt,
        "jti": jti_value,
        "exp": int(expire.timestamp())
    }
