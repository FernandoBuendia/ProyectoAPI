from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from archivos.database import User

secret_key = "my_secret_key"
algorithm = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/authentication")


def create_access_token(user, days=7):
    data = {
        "user_id": user.id,
        "username": user.username,
        "exp": datetime.now(timezone.utc) + timedelta(days=days),
    }

    return jwt.encode(data, secret_key, algorithm=algorithm)


def decode_access_token(token: str):
    try:
        return jwt.decode(token, secret_key, algorithms=[algorithm])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    data = decode_access_token(token)

    if data:
        return User.select().where(User.id == data["user_id"]).first()

    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
