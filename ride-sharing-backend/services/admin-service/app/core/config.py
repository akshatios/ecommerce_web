from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Ride Sharing Admin Service"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = "postgresql://postgres:password@db:5432/ride_sharing"
    
    # Service URLs
    AUTH_SERVICE_URL: str = "http://auth-service:8000"
    USER_SERVICE_URL: str = "http://user-service:8000"
    DRIVER_SERVICE_URL: str = "http://driver-service:8000"
    TRIP_SERVICE_URL: str = "http://trip-service:8000"
    PAYMENT_SERVICE_URL: str = "http://payment-service:8000"

    class Config:
        env_file = ".env"

settings = Settings()
