from fastapi import FastAPI
from app.core.config import settings
from app.api.v1 import location

app = FastAPI(title=settings.PROJECT_NAME)

@app.get("/")
def root():
    return {"message": "Welcome to Ride Sharing Location Service"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

app.include_router(location.router, prefix=f"{settings.API_V1_STR}/location", tags=["location"])
