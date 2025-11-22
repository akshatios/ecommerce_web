from passlib.context import CryptContext
from typing import Optional
import re

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class PasswordManager:
    """
    Helper class for password creation and verification
    Includes password strength validation
    """
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a plain password using bcrypt
        
        Args:
            password: Plain text password
        
        Returns:
            Hashed password
        """
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verify a plain password against hashed password
        
        Args:
            plain_password: Plain text password to verify
            hashed_password: Hashed password from database
        
        Returns:
            True if password matches, False otherwise
        """
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def validate_password_strength(password: str) -> tuple[bool, str]:
        """
        Validate password strength
        
        Requirements:
        - At least 8 characters
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one digit
        - At least one special character
        
        Args:
            password: Password to validate
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        
        if not re.search(r"[A-Z]", password):
            return False, "Password must contain at least one uppercase letter"
        
        if not re.search(r"[a-z]", password):
            return False, "Password must contain at least one lowercase letter"
        
        if not re.search(r"\d", password):
            return False, "Password must contain at least one digit"
        
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False, "Password must contain at least one special character"
        
        return True, "Password is strong"
    
    @staticmethod
    def validate_password_simple(password: str, min_length: int = 6) -> tuple[bool, str]:
        """
        Simple password validation (for less strict requirements)
        
        Args:
            password: Password to validate
            min_length: Minimum password length
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if len(password) < min_length:
            return False, f"Password must be at least {min_length} characters long"
        
        return True, "Password is valid"
    
    @staticmethod
    def create_and_verify(plain_password: str, use_strict_validation: bool = False) -> tuple[bool, str, Optional[str]]:
        """
        Create and verify password in one step
        
        Args:
            plain_password: Plain text password
            use_strict_validation: Use strict password validation
        
        Returns:
            Tuple of (is_valid, message, hashed_password)
        """
        # Validate password
        if use_strict_validation:
            is_valid, message = PasswordManager.validate_password_strength(plain_password)
        else:
            is_valid, message = PasswordManager.validate_password_simple(plain_password)
        
        if not is_valid:
            return False, message, None
        
        # Hash password
        hashed = PasswordManager.hash_password(plain_password)
        
        return True, "Password created successfully", hashed

# Convenience functions (backward compatible with utils.py)
def get_password_hash(password: str) -> str:
    """Hash password - backward compatible"""
    return PasswordManager.hash_password(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password - backward compatible"""
    return PasswordManager.verify_password(plain_password, hashed_password)

# Example usage:
# # Hash password
# hashed = PasswordManager.hash_password("MyPassword123!")
# 
# # Verify password
# is_valid = PasswordManager.verify_password("MyPassword123!", hashed)
# 
# # Validate and create
# is_valid, message, hashed = PasswordManager.create_and_verify("MyPassword123!", use_strict_validation=True)
