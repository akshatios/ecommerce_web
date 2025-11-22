from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.config import settings
from typing import List

class AllowedHostsMiddleware(BaseHTTPMiddleware):
    """
    Middleware to restrict access to specific hosts/domains
    Useful for preventing host header injection attacks
    """
    
    def __init__(self, app, allowed_hosts: List[str] = None):
        super().__init__(app)
        self.allowed_hosts = allowed_hosts or ["*"]
    
    async def dispatch(self, request: Request, call_next):
        # Get host from request
        host = request.headers.get("host", "").split(":")[0]
        
        # Allow all hosts if "*" is in allowed_hosts
        if "*" in self.allowed_hosts:
            return await call_next(request)
        
        # Check if host is allowed
        if host not in self.allowed_hosts:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid host header. Allowed hosts: {', '.join(self.allowed_hosts)}"
            )
        
        response = await call_next(request)
        return response

# Example usage in main.py:
# from app.middleware.allowedHostsMiddleware import AllowedHostsMiddleware
# app.add_middleware(AllowedHostsMiddleware, allowed_hosts=["localhost", "127.0.0.1", "yourdomain.com"])
