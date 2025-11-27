from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RiderCreate(BaseModel):
    user_id: int
    phone: str

class RiderResponse(BaseModel):
    id: int
    user_id: int
    phone: str
    wallet_balance: float
    rating: float
    created_at: datetime

    class Config:
        from_attributes = True
