from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status
import os
from datetime import timedelta, datetime
from dotenv import load_dotenv
from typing import Optional
from jose import jwt, JWTError


load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/authentication/token")


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.environ.get("SECRET_KEY"), algorithm=os.environ.get("ALGORITHM"))
    return encoded_jwt


def authenticate_user(username: str, password: str) -> None:
    USERNAME = os.environ.get("JWT_USERNAME")
    PASSWORD = os.environ.get("JWT_PASSWORD")
    if USERNAME == username and PASSWORD == password:
        return True
    return False


def verify_token(token: str = Depends(oauth2_scheme)) -> Optional[str]:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, os.environ.get("SECRET_KEY"), algorithms=[os.environ.get("ALGORITHM")])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        # You can include additional user checks here (e.g., is user active?)
        return username
    except JWTError:
        raise credentials_exception
