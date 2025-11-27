from fastapi import FastAPI
from app.core.config import settings
from app.api.v1 import driver
from app.core.database import engine, Base

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

@app.get("/")
def root():
    return {"message": "Welcome to Ride Sharing Driver Service"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

app.include_router(driver.router, prefix=f"{settings.API_V1_STR}/drivers", tags=["drivers"])
