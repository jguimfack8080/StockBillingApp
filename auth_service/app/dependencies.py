from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from .utils.security import decode_token
from .utils.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if not payload:
        raise credentials_exception

    user_data = {
        "email": payload.get("sub"),
        "role": payload.get("role")  
    }
    
    if not user_data["email"] or not user_data["role"]:
        raise credentials_exception

    return user_data
