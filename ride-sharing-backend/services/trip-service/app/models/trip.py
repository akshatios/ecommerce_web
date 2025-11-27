from sqlalchemy import Column, Integer, String, Float, DateTime, Enum
import enum
from datetime import datetime
from app.core.database import Base

class TripStatus(str, enum.Enum):
    REQUESTED = "REQUESTED"
    ASSIGNED = "ASSIGNED"
    STARTED = "STARTED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    rider_id = Column(Integer, index=True, nullable=False)
    driver_id = Column(Integer, index=True, nullable=True) # Initially null
    
    pickup_lat = Column(Float, nullable=False)
    pickup_lng = Column(Float, nullable=False)
    dropoff_lat = Column(Float, nullable=False)
    dropoff_lng = Column(Float, nullable=False)
    
    status = Column(String, default=TripStatus.REQUESTED)
    fare = Column(Float, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
