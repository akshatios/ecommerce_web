from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from app.core.config import settings
import secrets

class TokenCreator:
    """
    Helper class for creating and verifying JWT tokens
    Supports access tokens, refresh tokens, and custom tokens
    """
    
    def __init__(
        self,
        secret_key: str = None,
        algorithm: str = None,
        access_token_expire_minutes: int = None
    ):
        """
        Initialize Token Creator
        
        Args:
            secret_key: Secret key for encoding (defaults to settings)
            algorithm: Algorithm for encoding (defaults to settings)
            access_token_expire_minutes: Token expiration time (defaults to settings)
        """
        self.secret_key = secret_key or settings.SECRET_KEY
        self.algorithm = algorithm or settings.ALGORITHM
        self.access_token_expire_minutes = access_token_expire_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES
    
    def create_access_token(
        self,
        data: Dict[str, Any],
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Create JWT access token
        
        Args:
            data: Data to encode in token (e.g., {"sub": "username"})
            expires_delta: Custom expiration time
        
        Returns:
            Encoded JWT token
        """
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        
        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "access"
        })
        
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def create_refresh_token(
        self,
        data: Dict[str, Any],
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Create JWT refresh token (longer expiration)
        
        Args:
            data: Data to encode in token
            expires_delta: Custom expiration time (default: 7 days)
        
        Returns:
            Encoded JWT refresh token
        """
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(days=7)
        
        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "refresh"
        })
        
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Verify and decode JWT token
        
        Args:
            token: JWT token to verify
        
        Returns:
            Decoded token data or None if invalid
        """
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm]
            )
            return payload
        except JWTError:
            return None
    
    def decode_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Decode token without verification (for debugging)
        
        Args:
            token: JWT token to decode
        
        Returns:
            Decoded token data or None
        """
        try:
            payload = jwt.decode(
                token,
                options={"verify_signature": False}
            )
            return payload
        except JWTError:
            return None
    
    def is_token_expired(self, token: str) -> bool:
        """
        Check if token is expired
        
        Args:
            token: JWT token to check
        
        Returns:
            True if expired, False otherwise
        """
        payload = self.decode_token(token)
        if not payload:
            return True
        
        exp = payload.get("exp")
        if not exp:
            return True
        
        return datetime.fromtimestamp(exp) < datetime.utcnow()
    
    def get_token_expiry(self, token: str) -> Optional[datetime]:
        """
        Get token expiration datetime
        
        Args:
            token: JWT token
        
        Returns:
            Expiration datetime or None
        """
        payload = self.decode_token(token)
        if not payload:
            return None
        
        exp = payload.get("exp")
        if not exp:
            return None
        
        return datetime.fromtimestamp(exp)
    
    @staticmethod
    def generate_random_token(length: int = 32) -> str:
        """
        Generate random token (for password reset, email verification, etc.)
        
        Args:
            length: Token length
        
        Returns:
            Random token string
        """
        return secrets.token_urlsafe(length)

# Convenience function (backward compatible with utils.py)
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create access token - backward compatible"""
    creator = TokenCreator()
    return creator.create_access_token(data, expires_delta)

# Example usage:
# # Create token creator
# token_creator = TokenCreator()
# 
# # Create access token
# access_token = token_creator.create_access_token({"sub": "username"})
# 
# # Create refresh token
# refresh_token = token_creator.create_refresh_token({"sub": "username"})
# 
# # Verify token
# payload = token_creator.verify_token(access_token)
# 
# # Check if expired
# is_expired = token_creator.is_token_expired(access_token)
# 
# # Generate random token
# reset_token = TokenCreator.generate_random_token()
