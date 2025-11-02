from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status, Request, Cookie
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app import models

SECRET_KEY = "dev-secret-key-123456"

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Configure password context with bcrypt, disabling bug detection for compatibility
pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
   # Use bcrypt 2b format
)
security = HTTPBearer(auto_error=False)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> Optional[str]:
    """Extract username from token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        return username
    except JWTError:
        return None


def get_current_user_dependency(
    request: Request,
    access_token: Optional[str] = Cookie(None),
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token = None
    # Try to get token from cookie first
    if access_token:
        if access_token.startswith("Bearer "):
            token = access_token[7:]
        else:
            token = access_token
    # Also try from request cookies (for API calls)
    elif request and request.cookies.get("access_token"):
        cookie_token = request.cookies.get("access_token")
        if cookie_token.startswith("Bearer "):
            token = cookie_token[7:]
        else:
            token = cookie_token
    # Then try from Authorization header
    elif credentials:
        token = credentials.credentials
    
    if not token:
        raise credentials_exception
    
    username = decode_token(token)
    if username is None:
        raise credentials_exception

    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

# Alias for backward compatibility
get_current_user = get_current_user_dependency


async def get_current_user_optional(
    request: Request,
    db: Session = Depends(get_db)
) -> Optional[models.User]:
    # Try to get token from cookie
    access_token = request.cookies.get("access_token")
    if not access_token:
        return None
    
    # Remove "Bearer " prefix if present
    if access_token.startswith("Bearer "):
        token = access_token[7:]
    else:
        token = access_token
    
    username = decode_token(token)
    if username is None:
        return None
    
    user = db.query(models.User).filter(models.User.username == username).first()
    return user

