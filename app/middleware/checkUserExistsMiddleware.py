from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.database import db
from bson import ObjectId

class CheckUserExistsMiddleware(BaseHTTPMiddleware):
    """
    Middleware to check if authenticated user exists in database
    Validates user existence for protected routes
    """
    
    def __init__(self, app, excluded_paths: list = None):
        super().__init__(app)
        # Paths that don't require user existence check
        self.excluded_paths = excluded_paths or [
            "/",
            "/health",
            "/docs",
            "/redoc",
            "/openapi.json",
            "/register",
            "/login"
        ]
    
    async def dispatch(self, request: Request, call_next):
        # Skip check for excluded paths
        if any(request.url.path.startswith(path) for path in self.excluded_paths):
            return await call_next(request)
        
        # Get user from request state (set by authentication)
        user = getattr(request.state, "user", None)
        
        if user:
            # Verify user still exists in database
            user_id = user.get("_id") or user.get("id")
            
            if user_id:
                # Convert to ObjectId if string
                if isinstance(user_id, str):
                    user_id = ObjectId(user_id)
                
                # Check if user exists
                existing_user = db.users.find_one({"_id": user_id})
                
                if not existing_user:
                    raise HTTPException(
                        status_code=401,
                        detail="User no longer exists. Please login again."
                    )
                
                # Check if user is active
                if not existing_user.get("is_active", True):
                    raise HTTPException(
                        status_code=403,
                        detail="User account is deactivated"
                    )
        
        response = await call_next(request)
        return response

# Example usage in main.py:
# from app.middleware.checkUserExistsMiddleware import CheckUserExistsMiddleware
# app.add_middleware(CheckUserExistsMiddleware)
