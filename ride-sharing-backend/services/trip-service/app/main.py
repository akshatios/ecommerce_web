from fastapi import FastAPI
from app.core.config import settings
from app.api.v1 import trip
from app.core.database import engine, Base
from app.events.consumer import event_consumer, handle_payment_processed

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

@app.on_event("startup")
async def startup_event():
    """Initialize Kafka consumers on startup"""
    print("[STARTUP] Initializing Kafka consumers...")
    
    # Start consuming payment events
    event_consumer.start_consumer("payment.processed", handle_payment_processed)
    
    print("[STARTUP] Kafka consumers started")

@app.get("/")
def root():
    return {"message": "Welcome to Ride Sharing Trip Service"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

app.include_router(trip.router, prefix=f"{settings.API_V1_STR}/trips", tags=["trips"])
