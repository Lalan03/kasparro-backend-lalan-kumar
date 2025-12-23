# api/dependencies/auth.py
from fastapi import Header, HTTPException
from core.config import settings

def require_api_key(x_api_key: str = Header(...)):
    if x_api_key != settings.API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
