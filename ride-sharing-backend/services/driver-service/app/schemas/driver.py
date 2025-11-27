from pydantic import BaseModel
from typing import Optional

class VehicleBase(BaseModel):
    make: str
    model: str
    plate_number: str
    color: str

class VehicleCreate(VehicleBase):
    pass

class VehicleResponse(VehicleBase):
    id: int
    class Config:
        from_attributes = True

class DriverBase(BaseModel):
    license_number: str

class DriverCreate(DriverBase):
    user_id: int
    vehicle: VehicleCreate

class DriverResponse(DriverBase):
    id: int
    user_id: int
    is_verified: bool
    rating: float
    vehicle: Optional[VehicleResponse] = None

    class Config:
        from_attributes = True
