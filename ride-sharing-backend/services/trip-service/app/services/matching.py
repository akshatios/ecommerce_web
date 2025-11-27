import httpx
from app.core.config import settings

# In a real scenario, use service discovery or env vars for URLs
LOCATION_SERVICE_URL = "http://location-service:8000/api/v1/location"

async def find_nearby_drivers(lat: float, lng: float, radius_km: float = 5.0):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{LOCATION_SERVICE_URL}/nearby", params={"latitude": lat, "longitude": lng, "radius_km": radius_km})
            response.raise_for_status()
            return response.json().get("drivers", [])
        except Exception as e:
            print(f"Error fetching drivers: {e}")
            return []
