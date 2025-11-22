import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Application settings and configuration"""
    
    # MongoDB Configuration
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017/ecommerce_db")
    DATABASE_NAME: str = "ecommerce_db"
    
    # JWT Configuration
    SECRET_KEY: str = os.getenv("SECRET_KEY", "default_secret_key_change_in_production")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # Application Configuration
    APP_NAME: str = "E-commerce API"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "A complete e-commerce API built with FastAPI and MongoDB"
    
    # CORS Configuration
    CORS_ORIGINS: list = ["*"]  # In production, specify exact origins
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = 10
    MAX_PAGE_SIZE: int = 100

# Create settings instance
settings = Settings()
