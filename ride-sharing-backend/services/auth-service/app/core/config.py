from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Ride Sharing Auth Service"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "supersecretkey"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    DATABASE_URL: str = "postgresql://postgres:password@db:5432/ride_sharing"
    REDIS_URL: str = "redis://redis:6379/0"
    
    # OTP Settings
    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_PHONE_NUMBER: str = ""
    OTP_EXPIRE_MINUTES: int = 5

    class Config:
        env_file = ".env"

settings = Settings()
