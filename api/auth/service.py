# api/auth/service.py
from datetime import timedelta, datetime
from typing import Optional

from aiohttp.abc import HTTPException
from jose import JWTError, jwt
from plotly.io._orca import status

from api.auth.models import User

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return plain_password == hashed_password


def get_password_hash(password: str) -> str:
    return password  # Simplified for this example; use hashing in production


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> str:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception

        # Check token expiration
        expiration = payload.get("exp")
        if expiration is None or datetime.utcnow().timestamp() > expiration:
            raise credentials_exception

        return username
    except JWTError:
        raise credentials_exception
