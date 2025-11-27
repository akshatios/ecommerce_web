from fastapi import APIRouter, Depends
from app.schemas import LocationUpdate, LocationResponse
from app.core.redis import get_redis
import redis

router = APIRouter()

@router.post("/update", response_model=LocationResponse)
def update_location(location: LocationUpdate, redis_client: redis.Redis = Depends(get_redis)):
    # GEOADD key longitude latitude member
    # Storing in a key named "drivers_geo"
    redis_client.geoadd("drivers_geo", (location.longitude, location.latitude, str(location.driver_id)))
    
    # Also update a simple key for last seen info if needed
    # redis_client.set(f"driver:{location.driver_id}:last_seen", str(datetime.utcnow()))
    
    return {"status": "updated"}

@router.get("/nearby")
def get_nearby_drivers(latitude: float, longitude: float, radius_km: float = 5.0, redis_client: redis.Redis = Depends(get_redis)):
    # GEORADIUS key longitude latitude radius unit WITHDIST
    results = redis_client.georadius(
        "drivers_geo", 
        longitude, 
        latitude, 
        radius_km, 
        unit="km", 
        withdist=True
    )
    # Parse results: [(member, distance), ...]
    drivers = [{"driver_id": int(r[0]), "distance_km": r[1]} for r in results]
    return {"drivers": drivers}
