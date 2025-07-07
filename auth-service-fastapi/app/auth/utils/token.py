import logging
from jose import jwt, JWTError
from fastapi import status
from app.config import settings
from app.auth.exceptions import AuthException

logger = logging.getLogger(__name__)

def decode_token(token: str, expected_scope: str = None) -> dict:
  """
  Decode a JWT and optionally validate its scope.
  """
  try:
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    logger.info(f"Decoded JWT payload: {payload}")

    if expected_scope and payload.get("token_type") != expected_scope:
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
