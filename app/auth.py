from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status, Request, Cookie
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.config import (
    SECRET_KEY,
    JWT_ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ACCESS_COOKIE_NAME,
    AUTH_HEADER_PREFIX
)

# Alias for backward compatibility
ALGORITHM = JWT_ALGORITHM

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
security = HTTPBearer(auto_error=False)

def _strip_bearer(token: str) -> str:
    return token[len(AUTH_HEADER_PREFIX):] if token and token.startswith(AUTH_HEADER_PREFIX) else token

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None

def get_current_user_dependency(
    request: Request,
    access_token: Optional[str] = Cookie(None),
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> models.User:
    cred_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = None
    if access_token:
        token = _strip_bearer(access_token)
    elif request and request.cookies.get(ACCESS_COOKIE_NAME):
        token = _strip_bearer(request.cookies.get(ACCESS_COOKIE_NAME))
    elif credentials:
        token = credentials.credentials

    if not token:
        raise cred_exc

    username = decode_token(token)
    if not username:
        raise cred_exc

    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise cred_exc
    return user

get_current_user = get_current_user_dependency

async def get_current_user_optional(
    request: Request,
    db: Session = Depends(get_db)
) -> Optional[models.User]:
    token = request.cookies.get(ACCESS_COOKIE_NAME)
    if not token:
        return None
    username = decode_token(_strip_bearer(token))
    if not username:
        return None
    return db.query(models.User).filter(models.User.username == username).first()