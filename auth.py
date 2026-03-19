from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from datetime import datetime
import os
import logging
from dotenv import load_dotenv

load_dotenv()

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# In-memory session tracking
# Structure: { api_key: {"last_access": datetime, "request_count": int, "session_id": str} }
active_sessions = {}

# We require an explicitly configured API Key for strong security
VALID_API_KEY = os.getenv("API_KEY")
if not VALID_API_KEY or len(VALID_API_KEY) < 16:
    logger = logging.getLogger(__name__)
    logger.warning("API_KEY environment variable is not set or is too weak. Generating a single-session secure random key.")
    VALID_API_KEY = os.urandom(24).hex()
    logger.warning(f"Your temporary secure API_KEY for this run is: {VALID_API_KEY}")

def get_api_key(api_key_header: str = Security(api_key_header)) -> str:
    if not api_key_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key is missing",
        )
    
    if api_key_header != VALID_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate API Key",
        )
    
    # Session tracking
    now = datetime.now()
    if api_key_header not in active_sessions:
        active_sessions[api_key_header] = {
            "last_access": now,
            "request_count": 1,
            "session_id": f"sess_{int(now.timestamp())}"
        }
    else:
        active_sessions[api_key_header]["last_access"] = now
        active_sessions[api_key_header]["request_count"] += 1
        
    return api_key_header

def get_session_info(api_key: str) -> dict:
    return active_sessions.get(api_key, {})
