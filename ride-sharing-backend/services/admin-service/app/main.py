from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import admin

app = FastAPI(title=settings.PROJECT_NAME)

# Enable CORS for admin panel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your admin panel URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Welcome to Ride Sharing Admin Service"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

app.include_router(admin.router, prefix=f"{settings.API_V1_STR}/admin", tags=["admin"])
