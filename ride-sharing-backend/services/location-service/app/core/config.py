from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Ride Sharing Location Service"
    API_V1_STR: str = "/api/v1"
    REDIS_URL: str = "redis://redis:6379/0"
    KAFKA_BOOTSTRAP_SERVERS: str = "kafka:9092"

    class Config:
        env_file = ".env"

settings = Settings()
