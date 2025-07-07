from jose import jwt, JWTError
from fastapi import status
from app.config import settings
from app.exceptions import AuthException
import logging

logger = logging.getLogger(__name__)

def decode_token(authorization: str, expected_scope: str = None) -> dict:
  try:
    if authorization.startswith("Bearer "):
      token = authorization.split(" ")[1]
    else:
      token = authorization

    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

    if expected_scope and payload.get("scope") != expected_scope:
      raise AuthException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Invalid token scope"
      )

    return payload

  except JWTError as e:
    logger.error(f"Token decoding failed: {e}")
    raise AuthException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail=f"Invalid token: {str(e)}"
    )
