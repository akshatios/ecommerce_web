from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Ride Sharing Pricing Service"
    API_V1_STR: str = "/api/v1"
    
    # Pricing parameters
    BASE_FARE: float = 50.0
    PER_KM_RATE: float = 15.0
    PER_MINUTE_RATE: float = 2.0
    SURGE_MULTIPLIER: float = 1.0  # Can be dynamic based on demand

    class Config:
        env_file = ".env"

settings = Settings()
