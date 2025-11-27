from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class DashboardStats(BaseModel):
    total_users: int
    total_drivers: int
    total_trips: int
    active_trips: int
    total_revenue: float
    today_trips: int

class UserStats(BaseModel):
    id: int
    email: Optional[str]
    phone: Optional[str]
    full_name: Optional[str]
    role: str
    is_active: bool
    created_at: datetime

class TripStats(BaseModel):
    id: int
    rider_id: int
    driver_id: Optional[int]
    status: str
    fare: Optional[float]
    created_at: datetime
    pickup_lat: float
    pickup_lng: float
    dropoff_lat: float
    dropoff_lng: float

class RevenueStats(BaseModel):
    date: str
    total_trips: int
    total_revenue: float
    average_fare: float
