from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Ride Sharing Notification Service"
    API_V1_STR: str = "/api/v1"
    REDIS_URL: str = "redis://redis:6379/0"
    KAFKA_BOOTSTRAP_SERVERS: str = "kafka:9092"
    # FCM/APNs credentials would go here
    FCM_SERVER_KEY: str = ""

    class Config:
        env_file = ".env"

settings = Settings()
