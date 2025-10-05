from fastapi import Header, HTTPException, status
from typing import Optional

from app.core.config import settings
from app.core.security import verify_token

async def get_token_header(x_token: str = Header(...)):
    """Verify API token"""
    if not verify_token(x_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

async def get_query_token(token: str):
    """Verify query token (alternative authentication)"""
    if token != settings.SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )