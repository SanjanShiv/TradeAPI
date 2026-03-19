from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import Request

def get_rate_limit_key(request: Request):
    """Rate limit based on API Key (session) or IP if missing"""
    return request.headers.get("X-API-Key", get_remote_address(request))

# Rate Limiter based on the API Key
limiter = Limiter(key_func=get_rate_limit_key)
