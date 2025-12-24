# ============================================================
# COMBINED FILE: main.py
# This file combines:
#   1. google_oauth.py
#   2. auth_utils.py
#   3. main.py
# ============================================================

import os
from datetime import datetime, timedelta

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from jose import jwt, JWTError


# ============================================================
# [google_oauth.py] - Google OAuth Token Verification
# ============================================================

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")

def verify_google_id_token(token: str):
    """
    Verify Google ID token with Google servers
    (Originally from google_oauth.py)
    """
    try:
        idinfo = id_token.verify_oauth2_token(
            token,
            google_requests.Request(),
            GOOGLE_CLIENT_ID
        )
        return idinfo
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="無效的 Google Token"
        )


# ============================================================
# [auth_utils.py] - JWT Utilities
# ============================================================

SECRET_KEY = os.getenv("SECRET_KEY", "fallback-for-dev")
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/google")

def create_access_token(data: dict):
    """
    Create JWT access token
    (Originally from auth_utils.py)
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user_email(token: str = Depends(oauth2_scheme)):
    """
    Decode JWT and extract user email
    (Originally from auth_utils.py)
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token 缺少使用者資訊"
            )
        return email
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="JWT 驗證失敗"
        )


# ============================================================
# [main.py] - FastAPI Application & Routes
# ============================================================

app = FastAPI(title="資工系 114-Backend 示範專案")

class TokenRequest(BaseModel):
    """
    Request model for Google OAuth login
    (Originally from main.py)
    """
    id_token: str


@app.post("/auth/google", summary="Google OAuth 登入驗證")
async def google_auth(request: TokenRequest):
    """
    Exchange Google ID token for local JWT
    (Originally from main.py)
    """
    # Step A: Google token verification
    user_info = verify_google_id_token(request.id_token)

    # Step B: Extract email
    user_email = user_info.get("email")
    if not user_email:
        raise HTTPException(
            status_code=400,
            detail="Google 帳號未提供 Email"
        )

    # Step C: Issue local JWT
    access_token = create_access_token(
        data={"sub": user_email}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "name": user_info.get("name"),
            "email": user_email,
            "picture": user_info.get("picture")
        }
    }


@app.get("/users/me", summary="取得當前使用者資訊")
async def read_users_me(
    current_user: str = Depends(get_current_user_email)
):
    """
    Protected route using JWT
    (Originally from main.py)
    """
    return {
        "msg": "成功通過 JWT 驗證",
        "user_email": current_user
    }


@app.get("/")
def root():
    """
    Public test route
    (Originally from main.py)
    """
    return {"message": "Hello FastAPI OAuth Demo"}
