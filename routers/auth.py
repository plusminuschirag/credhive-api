import os
from datetime import timedelta
from dotenv import load_dotenv

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, Request, status
from .authentication.authenticate import authenticate_user, create_access_token
from clients.rate_limiting_client import limiter


load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/authentication/token")

router = APIRouter()


@router.post("/token", summary="Generate JWT Token for Subsequent Requests", tags=["Authentication"])
@limiter.limit("10/minute")
async def login_for_access_token(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")))
    access_token = create_access_token(data={"sub": form_data.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
