from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.middleware.base import BaseHTTPMiddleware
from jose import JWTError, jwt
from app.core.config import settings
from app.core.database import db
from bson import ObjectId
from typing import Optional

security = HTTPBearer()

class TokenAuthenticationMiddleware(BaseHTTPMiddleware):
    """
    Middleware for JWT token authentication
    Validates token and attaches user to request state
    """
    
    def __init__(self, app, excluded_paths: list = None):
        super().__init__(app)
        # Paths that don't require authentication
        self.excluded_paths = excluded_paths or [
            "/",
            "/health",
            "/docs",
            "/redoc",
            "/openapi.json",
            "/register",
            "/login"
        ]
    
    def verify_token(self, token: str) -> Optional[dict]:
        """
        Verify JWT token and return user data
        """
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
            username: str = payload.get("sub")
            
            if username is None:
                return None
            
            # Get user from database
            user = db.users.find_one({"username": username})
            return user
            
        except JWTError:
            return None
    
    async def dispatch(self, request: Request, call_next):
        # Skip authentication for excluded paths
        if any(request.url.path.startswith(path) for path in self.excluded_paths):
            return await call_next(request)
        
        # Get authorization header
        auth_header = request.headers.get("Authorization")
        
        if not auth_header:
            # Allow request to proceed (route-level auth will handle it)
            return await call_next(request)
        
        # Extract token
        try:
            scheme, token = auth_header.split()
            if scheme.lower() != "bearer":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication scheme"
                )
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization header format"
            )
        
        # Verify token
        user = self.verify_token(token)
        
        if user:
            # Attach user to request state
            request.state.user = user
        
        response = await call_next(request)
        return response

# Example usage in main.py:
# from app.middleware.tokenAuthentication import TokenAuthenticationMiddleware
# app.add_middleware(TokenAuthenticationMiddleware)
