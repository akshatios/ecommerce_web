from fastapi import FastAPI
from app.core.config import settings
from app.api.v1 import auth
from app.core.database import engine, Base

# Create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json")

@app.get("/")
def root():
    return {"message": "Welcome to Ride Sharing Auth Service"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
