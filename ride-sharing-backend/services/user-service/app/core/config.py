from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Ride Sharing User Service"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = "postgresql://postgres:password@db:5432/ride_sharing"

    class Config:
        env_file = ".env"

settings = Settings()
