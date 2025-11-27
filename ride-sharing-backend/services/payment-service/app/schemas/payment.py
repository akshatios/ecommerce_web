from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PaymentCreate(BaseModel):
    trip_id: int
    rider_id: int
    driver_id: int
    amount: float
    method: str = "CARD"

class PaymentResponse(BaseModel):
    id: int
    trip_id: int
    rider_id: int
    driver_id: int
    amount: float
    method: str
    status: str
    transaction_id: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
