from pydantic import BaseModel

class LocationUpdate(BaseModel):
    driver_id: int
    latitude: float
    longitude: float

class LocationResponse(BaseModel):
    status: str
