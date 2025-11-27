from fastapi import APIRouter
from pydantic import BaseModel
from app.services.pricing import calculate_fare

router = APIRouter()

class FareRequest(BaseModel):
    pickup_lat: float
    pickup_lng: float
    dropoff_lat: float
    dropoff_lng: float
    estimated_time_minutes: float = 0

@router.post("/calculate")
def get_fare_estimate(request: FareRequest):
    fare_details = calculate_fare(
        request.pickup_lat,
        request.pickup_lng,
        request.dropoff_lat,
        request.dropoff_lng,
        request.estimated_time_minutes
    )
    return fare_details
