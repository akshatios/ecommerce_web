from fastapi import FastAPI
from app.core.config import settings
from app.api.v1 import notify

app = FastAPI(title=settings.PROJECT_NAME)

@app.get("/")
def root():
    return {"message": "Welcome to Ride Sharing Notification Service"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

app.include_router(notify.router, prefix=f"{settings.API_V1_STR}/notifications", tags=["notifications"])
