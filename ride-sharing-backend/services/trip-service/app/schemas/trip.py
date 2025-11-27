from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TripRequest(BaseModel):
    rider_id: int
    pickup_lat: float
    pickup_lng: float
    dropoff_lat: float
    dropoff_lng: float

class TripResponse(BaseModel):
    id: int
    rider_id: int
    driver_id: Optional[int]
    status: str
    fare: Optional[float]
    created_at: datetime

    class Config:
        from_attributes = True
