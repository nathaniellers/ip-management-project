from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_data = payload.get("user")
        if user_data is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_data
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
